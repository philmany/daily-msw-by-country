import pandas as pd, numpy as np
import sys,os
W=sys.argv[1].rstrip('/')+'/' if len(sys.argv)>1 else 'input/'
OUT=sys.argv[2].rstrip('/')+'/' if len(sys.argv)>2 else 'data/'
raw=pd.read_excel(W+'What_a_Waste_3.0_COUNTRY_Dataset_&_Codebook.xlsx',sheet_name='Country dataset',header=0)
cols=list(raw.columns)
df=raw.iloc[1:].copy()   # row 0 holds machine names
df.columns=[c.strip() for c in cols]
g=lambda name:[c for c in df.columns if c.startswith(name)][0]
d=pd.DataFrame({
 'iso3':df['Country code'].astype(str).str.strip(),
 'waw_name':df['Country name'],
 'region':df['Region'],
 'income_2022':df['Income group (2022)'],
 'rep_year':pd.to_numeric(df['MSW generation - year reported'],errors='coerce'),
 'rep_t':pd.to_numeric(df['MSW generation (t/y)'],errors='coerce'),
 'rep_point':df['MSW generation - point of measurement'],
 'pop_gen':pd.to_numeric(df['Population in waste generation year'],errors='coerce'),
 'rep_kgcd':pd.to_numeric(df['MSW generation (kg/capita/day)'],errors='coerce'),
 'proj22_t':pd.to_numeric(df['MSW generation - projected 2022 (t/year)'],errors='coerce'),
 'pop22':pd.to_numeric(df['Population in 2022'],errors='coerce'),
})
c=pd.read_csv(W+'country-codes.csv',dtype=str)
ref=c[(c['is_independent']=='Yes')&(c['ISO3166-1-Alpha-3']!='TWN')|(c['ISO3166-1-Alpha-3']=='PSE')]
ref=ref[['ISO3166-1-Alpha-3','CLDR display name']].rename(columns={'ISO3166-1-Alpha-3':'iso3','CLDR display name':'country'})
ref['status']=np.where(ref.iso3.isin(['VAT','PSE']),'UN observer','UN member')
print(len(ref),'reference countries;',len(d),'WAW rows; dup iso',d.iso3.duplicated().sum())
m=ref.merge(d,on='iso3',how='left',indicator=True)
rows=[];log=[]
for _,r in m.iterrows():
    base=dict(iso3=r.iso3,country=r.country,status=r.status)
    if r._merge=='left_only':
        log.append({**base,'reason':'Not present in World Bank What a Waste 3.0 country file'});continue
    ok_rep=pd.notna(r.rep_year) and r.rep_year>=2022 and pd.notna(r.rep_t) and r.rep_t>0
    ok_mod=pd.notna(r.proj22_t) and r.proj22_t>0
    if ok_rep:
        t,y,b=r.rep_t,int(r.rep_year),'reported'
        note=''
    elif ok_mod:
        t,y,b=r.proj22_t,2022,'modelled (World Bank 2022 baseline)'
        if pd.notna(r.rep_year) and pd.notna(r.rep_t): note=f'Reported figure is from {int(r.rep_year)} (older than cutoff); modelled 2022 value used'
        else: note='No reported national figure; modelled 2022 value used'
    else:
        why=[]
        if pd.isna(r.rep_t) or r.rep_t<=0: why.append('no reported MSW total')
        elif pd.isna(r.rep_year) or r.rep_year<2022: why.append(f'reported total is from {"unknown year" if pd.isna(r.rep_year) else int(r.rep_year)} (before 2022)')
        why.append('no usable modelled 2022 value')
        log.append({**base,'reason':'; '.join(why)});continue
    pop=r.pop22 if b!='reported' else r.pop_gen
    kgcd=t*1000/pop/365 if pd.notna(pop) and pop>0 else np.nan
    flag=''
    if pd.notna(kgcd) and (kgcd>2.5 or kgcd<0.05): flag='check: implausible kg/person/day'
    rows.append({**base,'region':r.region,'income_group_2022':r.income_2022,'data_year':y,'data_basis':b,
      'annual_tonnes':round(t,2),'tonnes_per_day':round(t/365,2),'kg_per_person_per_day':round(kgcd,3) if pd.notna(kgcd) else np.nan,
      'point_of_measurement':r.rep_point if b=='reported' else '','flag':flag,'note':note})
out=pd.DataFrame(rows).replace({'country':{'US':'United States','UK':'United Kingdom'}}).sort_values('country').reset_index(drop=True)
lg=pd.DataFrame(log).sort_values('country').reset_index(drop=True)
out.to_csv(OUT+'daily_msw_tonnes_by_country.csv',index=False)
lg.to_csv(OUT+'exclusion_log.csv',index=False)
print(len(out),'included;',len(lg),'excluded')
print(out.data_basis.value_counts()); print(out.data_year.value_counts().sort_index())
print(out[out.flag!=''][['country','tonnes_per_day','kg_per_person_per_day','data_basis']])
print(lg.to_string())
print('world total t/day',out.tonnes_per_day.sum())
