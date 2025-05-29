from Bio import Entrez,SeqIO;import pandas as pd,matplotlib.pyplot as plt,time,os
def main():
 try:e,k,t=input("Email API key taxid: ").split();mn,mx,mr=map(int,input("minL maxL maxR: ").split())
 except:mn,mx,mr=0,10000000,50
 Entrez.email,Entrez.api_key,Entrez.tool=e,k,'G'
 try:o=Entrez.read(Entrez.efetch("taxonomy",id=t,retmode="xml"))[0]["ScientificName"];term=f"txid{t}[Organism] AND {int(mn)}:{int(mx)}[Sequence Length]";res=Entrez.read(Entrez.esearch("nucleotide",term=term,usehistory="y"));c=int(res["Count"]);assert c>0;w,q,c=res["WebEnv"],res["QueryKey"],c
 except Exception as e:print("err:",e);return
 data=[]
 for st in range(0,min(c,mr),20):
  try:
   h=Entrez.efetch("nucleotide",rettype="gb",retmode="text",retstart=st,retmax=20,webenv=w,query_key=q)
   data+=[{"a":r.id,"l":len(r.seq),"d":r.description} for r in SeqIO.parse(h,"gb")]
   time.sleep(0.4)
  except Exception as e:print(f"err {st}:",e)
 if not data: return print("err")
 pd.DataFrame(data).to_csv("g.csv",index=False);
 df=pd.DataFrame(data).sort_values("l",ascending=False)
 fig,ax=plt.subplots(figsize=(12,6));ax.plot(df["a"],df["l"],marker='o')
 ax.set(xlabel="Accn", ylabel="Len", title="Seq Leng")
 plt.xticks(rotation=90);plt.tight_layout();plt.savefig("s.png");plt.close();
if __name__=="__main__":main()
