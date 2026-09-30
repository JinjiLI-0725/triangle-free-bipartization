// Only the Y already recorded in the saved H0 witness table is examined.
#include <bits/stdc++.h>
#include <filesystem>
using namespace std;
vector<string> split(const string&s,char d='\t'){vector<string> r;string x;istringstream in(s);while(getline(in,x,d))r.push_back(x);return r;}
string format_list(const vector<int>&v,int inf=1000000){string s;for(int x:v){if(!s.empty())s+=",";s+=x==inf?"NA":to_string(x);}return s;}
int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage: checker saved_h0_witnesses.tsv NEW_output.tsv\n";return 2;}
 if(filesystem::exists(argv[2]))throw runtime_error("refusing overwrite");
 ifstream in(argv[1]);if(!in)throw runtime_error("input missing");ofstream out(argv[2]);if(!out)throw runtime_error("output missing");
 out<<"id\tgraph6\tY_mask\tdG\tdH\tq\tF\tattaining_global_masks\tcontiguous\tadjacent_lower_lipschitz\tconvex_finite_triples\tF_min_at_zero\tF_nondecreasing\tcombined_nondecreasing\tfirst_slope_failure\tfirst_convex_failure\n";
 string line;getline(in,line);set<int> ids;int done=0;const int INF=1000000;
 while(getline(in,line)){
  auto r=split(line);if(r.size()!=12)throw runtime_error("input columns");int id=stoi(r[0]),Y=stoi(r[2]),savedF=stoi(r[4]),savedDG=stoi(r[6]),savedDH=stoi(r[7]);
  if(!ids.insert(id).second)throw runtime_error("duplicate id");string g6=r[1];if(g6[0]-63!=15||__builtin_popcount((unsigned)Y)!=5)throw runtime_error("not saved n15 witness");
  array<int,15> a{},b{};int bit=0,m=0,mH=0,H=32767^Y;
  for(int j=1;j<15;j++)for(int i=0;i<j;i++,bit++)if(((g6.at(1+bit/6)-63)>>(5-bit%6))&1){a[i]|=1<<j;a[j]|=1<<i;m++;if((H>>i&1)&&(H>>j&1)){b[i]|=1<<j;b[j]|=1<<i;mH++;}}
  for(int v=0;v<15;v++)for(int u=v+1;u<15;u++)if((a[v]>>u&1)&&(a[v]&a[u]))throw runtime_error("triangle");
  vector<int> gc(16384),hc(16384);gc[0]=m;hc[0]=mH;
  int dg=m,dh=mH;
  for(int s=1;s<16384;s++){int v=__builtin_ctz((unsigned)s)+1,p=s^(1<<(v-1));gc[s]=gc[p]-__builtin_popcount((unsigned)a[v])+2*__builtin_popcount((unsigned)(a[v]&(p<<1)));hc[s]=hc[p]-__builtin_popcount((unsigned)b[v])+2*__builtin_popcount((unsigned)(b[v]&(p<<1)));dg=min(dg,gc[s]);dh=min(dh,hc[s]);}
  if(dg!=savedDG||dh!=savedDH||dg-dh!=stoi(r[8]))throw runtime_error("saved d mismatch");
  int f=savedF;if(f&1)f^=32767;if(gc[f>>1]!=dg||hc[f>>1]!=dh)throw runtime_error("saved witness not inherited optimum");
  vector<int> F(mH-dh+1,INF),masks(F.size(),INF);
  for(int s=0;s<16384;s++){int j=hc[s]-dh,cost=gc[s]-hc[s];if(cost<F[j]){F[j]=cost;masks[j]=s<<1;}}
  if(F[0]!=dg-dh||F[0]>5)throw runtime_error("H0 identity failure");
  bool contiguous=true,slope=true,convex=true,minzero=true,nondec=true,gnd=true;int fs=-1,fc=-1;
  for(int j=0;j<(int)F.size();j++){
   if(F[j]==INF){contiguous=false;continue;}
   if(j+F[j]<F[0])throw runtime_error("anchored inequality failure");
   minzero&=F[j]>=F[0];
   if(j&&F[j-1]!=INF){if(F[j]<F[j-1]-1){slope=false;if(fs<0)fs=j-1;}nondec&=F[j]>=F[j-1];gnd&=j+F[j]>=j-1+F[j-1];}
   if(j>=2&&F[j-1]!=INF&&F[j-2]!=INF&&F[j]+F[j-2]<2*F[j-1]){convex=false;if(fc<0)fc=j-2;}
  }
  out<<id<<'\t'<<g6<<'\t'<<Y<<'\t'<<dg<<'\t'<<dh<<'\t'<<dg-dh<<'\t'<<format_list(F)<<'\t'<<format_list(masks)<<'\t'<<contiguous<<'\t'<<slope<<'\t'<<convex<<'\t'<<minzero<<'\t'<<nondec<<'\t'<<gnd<<'\t'<<fs<<'\t'<<fc<<'\n';
  if(++done%500==0){out.flush();cerr<<"saved witnesses completed "<<done<<"\n";}
 }
 cerr<<"DONE "<<done<<" saved witness frontiers\n";
}
