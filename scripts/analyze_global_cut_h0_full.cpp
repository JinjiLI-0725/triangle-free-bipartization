// Full-corpus driver sharing the validated landscape primitives.
#define GLOBAL_LANDSCAPE_NO_MAIN
#include "analyze_global_cut_landscape_n15.cpp"
#ifdef __BMI2__
#include <immintrin.h>
#endif

unsigned project(unsigned x,unsigned mask){
#ifdef __BMI2__
 return _pext_u32(x,mask);
#else
 unsigned r=0,b=1;while(mask){unsigned bit=mask&-mask;if(x&bit)r|=b;mask-=bit;b<<=1;}return r;
#endif
}
int canonical10(int x){return ((x&1)?(x^1023):x)>>1;}
vector<int> canonical_costs(const vector<int>& a){
 int n=a.size(),m=0;for(int x:a)m+=pc(x);m/=2;
 vector<int> c(1<<(n-1));c[0]=m;
 for(int x=1;x<(int)c.size();x++){int bit=__builtin_ctz((unsigned)x),v=bit+1,p=x^(1<<bit);c[x]=c[p]-pc(a[v])+2*pc(a[v]&(p<<1));}
 return c;
}
const string HEADER="id\tgraph6\tdG\tm\tL\toptG_count\td_edge_critical\tfive_sets\tgood_count\tbad_count\tmin_q\tgood_min_rho\tgood_min_delta\tgood_rho0\tgood_rho1\tgood_rho2\tgood_rho3\tgood_rho4\tgood_rho5\tidentities_checked";
const string WHEADER="id\tgraph6\tY_mask\tY_vertices\tf_mask\th_local\tdG\tdH\tq\tR\tDelta\trho";
int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage: full_checker corpus.txt output_dir\n";return 2;}
 fs::path out=argv[2],cp=out/"checkpoints";fs::create_directories(cp);
 if(fs::exists(out/"FIRST_FAILURE")){cerr<<"Prior failure exists; refusing to continue\n";return 3;}
 ifstream in(argv[1]);if(!in)throw runtime_error("missing input");
 vector<int> ys;for(int x=0;x<32768;x++)if(pc(x)==5)ys.push_back(x);
 array<unsigned long long,512> cut_masks{};
 for(int h=0;h<512;h++){int f=h<<1,bit=0;for(int j=1;j<10;j++)for(int i=0;i<j;i++,bit++)if(((f>>i)^(f>>j))&1)cut_masks[h]|=1ULL<<bit;}
 array<vector<int>,6> shells;for(int x=1;x<1024;x++)if(pc(x)<=5)shells[pc(x)].push_back(x);
 Graph g;int unused,processed=0;auto started=chrono::steady_clock::now();
 while(in>>g.id>>g.g6>>g.n>>g.m>>unused){
  g.es.clear();g.adj.fill(0);for(int j=0;j<g.m;j++){int u,v;in>>u>>v;g.es.push_back({u,v});g.adj[u]|=1<<v;g.adj[v]|=1<<u;}
  if(g.n!=15)throw runtime_error("not n15");
  for(auto[u,v]:g.es)if(g.adj[u]&g.adj[v])throw runtime_error("triangle");
  string stem=to_string(g.id);if(fs::exists(cp/(stem+".done"))){cerr<<"resume "<<g.id<<"\n";continue;}
  vector<int> adj(g.adj.begin(),g.adj.end()),gc=canonical_costs(adj),opt;
  int dG=*min_element(gc.begin(),gc.end());for(int i=0;i<(int)gc.size();i++)if(gc[i]==dG)opt.push_back(i<<1);
  bool critical=true;for(auto[u,v]:g.es){bool yes=false;for(int f:opt)if((((f>>u)^(f>>v))&1)==0){yes=true;break;}critical&=yes;}
  vector<unsigned char> packed;packed.reserve(9009);
  int minq=99,minrho=99,mindelta=99,L=999,good=0,bad=0,wY=-1,wF=-1,wH=-1,wq=-1,wdH=-1;
  array<int,6> rhog{};long long identities=0;
  for(int Y:ys){int H=Y^32767;auto hv=verts(H);vector<int>ha(10);for(int j=0;j<10;j++)ha[j]=project(g.adj[hv[j]],H);
   unsigned long long edge_mask=0;int bit=0;for(int j=1;j<10;j++){edge_mask|=(unsigned long long)(ha[j]&((1<<j)-1))<<bit;bit+=j;}
   int eH=__builtin_popcountll(edge_mask),dH=eH;array<unsigned char,512> hc;
   for(int c=0;c<512;c++){int value=eH-__builtin_popcountll(edge_mask&cut_masks[c]);hc[c]=value;dH=min(dH,value);}
   int q=dG-dH,dm=99,compatible=0,firstf=-1;
   vector<int> projections;projections.reserve(opt.size());
   for(int f:opt){int p=canonical10(project(f,H));int delta=hc[p]-dH,R=dG-hc[p];if(delta<0||R<0||R+delta!=q)throw runtime_error("identity");identities++;dm=min(dm,delta);if(!delta){compatible++;if(firstf<0)firstf=f;}projections.push_back(p);}
   int rho=0;
   if(dm){sort(projections.begin(),projections.end());projections.erase(unique(projections.begin(),projections.end()),projections.end());bool found=false;
    for(int r=1;r<=5&&!found;r++)for(int p:projections){for(int flip:shells[r])if(hc[canonical10((p<<1)^flip)]==dH){rho=r;found=true;break;}if(found)break;}
    if(!found)throw runtime_error("no nearest cut at distance <=5");
   }
   if((rho==0)!=(dm==0)||(dm==0)!=(compatible>0))throw runtime_error("rho equivalence");
   packed.push_back(dH);packed.push_back(dm);packed.push_back(rho);
   int ds=0,twice=0;bool c5=true;for(int v:verts(Y)){ds+=pc(g.adj[v]);int id=pc(g.adj[v]&Y);twice+=id;c5&=id==2;}L=min(L,ds-twice+2*c5);
   minq=min(minq,q);if(q<=5){good++;minrho=min(minrho,rho);mindelta=min(mindelta,dm);rhog[rho]++;if(dm==0&&wY<0){wY=Y;wF=firstf;wH=project(firstf,H);wq=q;wdH=dH;}}else bad++;
  }
  if(packed.size()!=9009||good+bad!=3003)throw runtime_error("count");
  {ofstream o(cp/(stem+".landscape.tmp"),ios::binary);o.write((char*)packed.data(),packed.size());}
  {ofstream o(cp/(stem+".opt.tmp"));o<<join(opt)<<'\n';}
  {ofstream o(cp/(stem+".summary.tmp"));o<<HEADER<<'\n'<<g.id<<'\t'<<g.g6<<'\t'<<dG<<'\t'<<g.m<<'\t'<<L<<'\t'<<opt.size()<<'\t'<<critical<<"\t3003\t"<<good<<'\t'<<bad<<'\t'<<minq<<'\t'<<minrho<<'\t'<<mindelta;for(int x:rhog)o<<'\t'<<x;o<<'\t'<<identities<<'\n';}
  {ofstream o(cp/(stem+".witness.tmp"));o<<WHEADER<<'\n';if(wY>=0)o<<g.id<<'\t'<<g.g6<<'\t'<<wY<<'\t'<<join(verts(wY))<<'\t'<<wF<<'\t'<<wH<<'\t'<<dG<<'\t'<<wdH<<'\t'<<wq<<'\t'<<wq<<"\t0\t0\n";}
  for(string type:{"landscape","opt","summary","witness"})fs::rename(cp/(stem+"."+type+".tmp"),cp/(stem+"."+type+(type=="landscape"?".bin":type=="opt"?".txt":".tsv")));
  {ofstream done(cp/(stem+".done"));done<<g.g6<<" 3003 exact\n";}
  processed++;double elapsed=chrono::duration<double>(chrono::steady_clock::now()-started).count();
  cerr<<"completed id="<<g.id<<" d="<<dG<<" L="<<L<<" H0="<<(wY>=0)<<" min_delta="<<mindelta<<" min_rho="<<minrho<<" processed="<<processed<<" elapsed="<<elapsed<<"s\n";
  if(wY<0){
   ofstream o(out/"failure_fivesets.tsv");o<<"id\tY_mask\tdH\tq\tdelta_min\trho\n";for(int j=0;j<3003;j++)o<<g.id<<'\t'<<ys[j]<<'\t'<<int(packed[3*j])<<'\t'<<dG-int(packed[3*j])<<'\t'<<int(packed[3*j+1])<<'\t'<<int(packed[3*j+2])<<'\n';o.close();
   {ofstream o(out/"failure.graph6");o<<g.g6<<'\n';}
   {ofstream o(out/"FIRST_FAILURE");o<<g.id<<'\n';}
   cerr<<"STOP: first H0 failure "<<g.id<<"\n";return 3;
  }
 }
 cerr<<"COMPLETE newly analyzed="<<processed<<"\n";
}
