#include <bits/stdc++.h>
#include <filesystem>
using namespace std;
namespace fs=std::filesystem;
int pc(unsigned x){return __builtin_popcount(x);}
struct Graph{int id,n,m;string g6; vector<pair<int,int>> es;array<int,15> adj{};};
string join(const vector<int>& v){string s;for(int x:v){if(!s.empty())s+=",";s+=to_string(x);}return s.empty()?"-":s;}
vector<int> verts(int mask){vector<int> v;for(int i=0;i<15;i++)if(mask>>i&1)v.push_back(i);return v;}
vector<int> costs(const vector<int>&adj){int n=adj.size(),m=0;for(int a:adj)m+=pc(a);m/=2;vector<int> c(1<<n);c[0]=m;for(int x=1;x<(1<<n);x++){int v=__builtin_ctz((unsigned)x),p=x^(1<<v);c[x]=c[p]-pc(adj[v])+2*pc(adj[v]&p);}return c;}
int compress(int mask,const vector<int>&vs){int r=0;for(int j=0;j<(int)vs.size();j++)r|=((mask>>vs[j])&1)<<j;return r;}
int expand(int mask,const vector<int>&vs){int r=0;for(int j=0;j<(int)vs.size();j++)r|=((mask>>j)&1)<<vs[j];return r;}
array<int,1024> canon5;
void canonical_table(){for(int code=0;code<1024;code++){int a[5][5]={},b=0;for(int j=1;j<5;j++)for(int i=0;i<j;i++)a[i][j]=a[j][i]=(code>>b++)&1;array<int,5> p={0,1,2,3,4};int best=1024;do{int r=0,z=0;for(int j=1;j<5;j++)for(int i=0;i<j;i++)r|=a[p[i]][p[j]]<<z++;best=min(best,r);}while(next_permutation(p.begin(),p.end()));canon5[code]=best;}}
struct Shape{int n=0,m=0,connected=0,path=0,star=0,bip=1;string degrees;};
Shape shape(const Graph&g,int s){Shape a;auto vs=verts(s);a.n=vs.size();vector<int>d;for(int v:vs){d.push_back(pc(g.adj[v]&s));a.m+=d.back();}a.m/=2;sort(d.begin(),d.end());a.degrees=join(d);if(!s)return a;int seen=0;array<int,15> col;col.fill(-1);int components=0;for(int v:vs)if(col[v]<0){components++;queue<int>q;q.push(v);col[v]=0;while(!q.empty()){int u=q.front();q.pop();seen|=1<<u;for(int w:vs)if(g.adj[u]>>w&1){if(col[w]<0){col[w]=col[u]^1;q.push(w);}else if(col[w]==col[u])a.bip=0;}}}a.connected=components==1;a.path=a.connected&&a.m==a.n-1&&d.back()<=2;a.star=a.connected&&a.m==a.n-1&&d.back()==a.n-1;return a;}
#ifndef GLOBAL_LANDSCAPE_NO_MAIN
int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage: checker sample_input.txt output_dir\n";return 2;}
 canonical_table();fs::path out=argv[2];fs::create_directories(out/"checkpoints");ifstream in(argv[1]);if(!in)throw runtime_error("input missing");
 Graph g;int unused,done=0;while(in>>g.id>>g.g6>>g.n>>g.m>>unused){g.es.clear();g.adj.fill(0);for(int i=0;i<g.m;i++){int u,v;in>>u>>v;g.es.push_back({u,v});g.adj[u]|=1<<v;g.adj[v]|=1<<u;}if(g.n!=15)throw runtime_error("not n=15");for(auto[u,v]:g.es)if(g.adj[u]&g.adj[v])throw runtime_error("not triangle free");
  string stem=to_string(g.id);fs::path dir=out/"checkpoints";if(fs::exists(dir/(stem+".done"))){cerr<<"resume skip "<<g.id<<"\n";continue;}
  vector<int> adj(g.adj.begin(),g.adj.end()),gc=costs(adj),opt;int dG=*min_element(gc.begin(),gc.end());for(int f=0;f<32768;f+=2)if(gc[f]==dG)opt.push_back(f);
  for(int f=0;f<32768;f++)if(gc[f]!=gc[f^32767])throw runtime_error("global reversal");
  bool critical=true;for(auto[u,v]:g.es){bool covered=false;for(int f:opt)if(((f>>u)^(f>>v))%2==0){covered=true;break;}critical&=covered;}
  ofstream five(dir/(stem+".five.tmp")),wit(dir/(stem+".witness.tmp")),cuts(dir/(stem+".cuts.tmp"));
  five<<"id\tY_mask\tdH\toptH_count\tq\tgood\tdelta_min\trho\tcompatible_optG\tell\tY_type\tY_edges\tdegree_sum\tf_witness\th_witness_local\tS_mask\tR_witness\tDelta_witness\toptH_masks_local\n";
  wit<<"id\tY_mask\tgood\tq\trho\tdelta_min\tf_mask\th_mask_local\tS_mask\tS_vertices\tS_size\tS_edges\tS_degrees\tindependent\tconnected\tpath\tstar\tbipartite\tH_boundary_M\tH_boundary_C\tY_boundary_M\tY_boundary_C\tS_internal_M\tS_internal_C\tR\tDelta\n";
  cuts<<"id\tdG\toptG_masks\n"<<g.id<<'\t'<<dG<<'\t'<<join(opt)<<'\n';
  int minq=99,minrho=99,mindelta=99,L=999,good=0,bad=0,ny=0;array<int,6> rhog{},rhob{};long long identities=0;
  for(int Y=0;Y<32768;Y++)if(pc(Y)==5){ny++;auto yv=verts(Y),hv=verts(Y^32767);vector<int> ha(10);for(int j=0;j<10;j++)ha[j]=compress(g.adj[hv[j]],hv);auto hc=costs(ha);int dH=*min_element(hc.begin(),hc.end());vector<int> oh;for(int h=0;h<1024;h+=2)if(hc[h]==dH)oh.push_back(h);
   array<int,1024> distance,nearest;distance.fill(99);nearest.fill(-1);queue<int> bfs;for(int h=0;h<1024;h++){if(hc[h]!=hc[h^1023])throw runtime_error("core reversal");if(hc[h]==dH){distance[h]=0;nearest[h]=h;bfs.push(h);}}
   while(!bfs.empty()){int x=bfs.front();bfs.pop();for(int i=0;i<10;i++){int z=x^(1<<i);if(distance[z]==99){distance[z]=distance[x]+1;nearest[z]=nearest[x];bfs.push(z);}}}
   int q=dG-dH,dm=99,rho=99,ncompat=0,bestf=-1,besth=-1,bestproj=-1;
   for(int f:opt){int p=compress(f,hv),de=hc[p]-dH,R=dG-hc[p];if(de<0||R+de!=q)throw runtime_error("q=R+Delta");identities++;dm=min(dm,de);ncompat+=de==0;int rr=distance[p];if(rr<rho){rho=rr;bestf=f;besth=nearest[p];bestproj=p;}}
   if((rho==0)!=(dm==0)||((rho==0)!=(ncompat>0)))throw runtime_error("rho equivalence");
   int S=expand(bestproj^besth,hv);if(pc(S)!=rho||rho>5)throw runtime_error("distance");int de=hc[bestproj]-dH,R=dG-hc[bestproj];
   int ey=0,code=0,bit=0,ds=0;bool c5=true;for(int v:yv){ds+=pc(g.adj[v]);c5&=pc(g.adj[v]&Y)==2;}for(int j=1;j<5;j++)for(int i=0;i<j;i++){bool edge=g.adj[yv[i]]>>yv[j]&1;ey+=edge;code|=edge<<bit++;}int ell=ds-2*ey+2*c5;L=min(L,ell);
   bool isgood=q<=5;minq=min(minq,q);if(isgood){good++;minrho=min(minrho,rho);mindelta=min(mindelta,dm);rhog[rho]++;}else{bad++;rhob[rho]++;}
   five<<g.id<<'\t'<<Y<<'\t'<<dH<<'\t'<<oh.size()<<'\t'<<q<<'\t'<<isgood<<'\t'<<dm<<'\t'<<rho<<'\t'<<ncompat<<'\t'<<ell<<'\t'<<canon5[code]<<'\t'<<ey<<'\t'<<ds<<'\t'<<bestf<<'\t'<<besth<<'\t'<<S<<'\t'<<R<<'\t'<<de<<'\t'<<join(oh)<<'\n';
   if(rho>0){auto sh=shape(g,S);int hm=0,hb=0,ym=0,yb=0,im=0,ib=0;for(auto[u,v]:g.es){bool mono=(((bestf>>u)^(bestf>>v))&1)==0;if((S>>u&1)&&(S>>v&1)){if(mono)im++;else ib++;}if((S>>u&1)!=(S>>v&1)){int other=(S>>u&1)?v:u;if(Y>>other&1){if(mono)ym++;else yb++;}else{if(mono)hm++;else hb++;}}}if(hm-hb!=de)throw runtime_error("switch gain");
    wit<<g.id<<'\t'<<Y<<'\t'<<isgood<<'\t'<<q<<'\t'<<rho<<'\t'<<dm<<'\t'<<bestf<<'\t'<<besth<<'\t'<<S<<'\t'<<join(verts(S))<<'\t'<<sh.n<<'\t'<<sh.m<<'\t'<<sh.degrees<<'\t'<<(sh.m==0)<<'\t'<<sh.connected<<'\t'<<sh.path<<'\t'<<sh.star<<'\t'<<sh.bip<<'\t'<<hm<<'\t'<<hb<<'\t'<<ym<<'\t'<<yb<<'\t'<<im<<'\t'<<ib<<'\t'<<R<<'\t'<<de<<'\n';
   }
  }
  if(ny!=3003)throw runtime_error("five-set count");five.close();wit.close();cuts.close();
  ofstream sum(dir/(stem+".summary.tmp"));sum<<"id\tgraph6\tdG\tm\tL\toptG_count\td_edge_critical\tfive_sets\tgood_count\tbad_count\tmin_q\tgood_min_rho\tgood_min_delta\tgood_rho0\tgood_rho1\tgood_rho2\tgood_rho3\tgood_rho4\tgood_rho5\tidentities_checked\n";
  sum<<g.id<<'\t'<<g.g6<<'\t'<<dG<<'\t'<<g.m<<'\t'<<L<<'\t'<<opt.size()<<'\t'<<critical<<'\t'<<ny<<'\t'<<good<<'\t'<<bad<<'\t'<<minq<<'\t'<<minrho<<'\t'<<mindelta;for(int x:rhog)sum<<'\t'<<x;sum<<'\t'<<identities<<'\n';sum.close();
  for(string kind:{"five","witness","cuts","summary"})fs::rename(dir/(stem+"."+kind+".tmp"),dir/(stem+"."+kind+".tsv"));ofstream mark(dir/(stem+".done"));mark<<"complete 3003 five-sets; exact all cuts\n";mark.close();cerr<<"completed id="<<g.id<<" d="<<dG<<" L="<<L<<" optG="<<opt.size()<<" minq="<<minq<<" good="<<good<<" minrho="<<minrho<<" identities="<<identities<<"\n";done++;
 }
 cerr<<"new graphs completed="<<done<<"\n";
}

#endif
