#define GLOBAL_LANDSCAPE_NO_MAIN
#include "analyze_global_cut_landscape_n15.cpp"
#include <charconv>

vector<string> split(const string&s,char c='\t'){vector<string>r;stringstream ss(s);string x;while(getline(ss,x,c))r.push_back(x);return r;}
void put(string&s,int x,bool tab=true){char b[32];auto r=to_chars(b,b+32,x);s.append(b,r.ptr);s+=tab?'\t':'\n';}
struct Meta{int d,L,opt,crit,good;string g6;};
struct Type{int edges,comp,dy,lo,hi;};
struct Row{int Y,q,dm,rho,ell,dy,ey,z,ds,lo,hi,type,comp,inherit,wf,ilo,ihi;bool good,h0;};
const vector<string> RULES={"min_ell","min_degree_sum","min_boundary","max_inherited_count","min_ell_then_max_inherited","min_degree_sum_then_max_inherited","min_boundary_then_max_inherited","max_inherited_then_min_ell","max_inherited_then_min_degree_sum","max_inherited_then_min_boundary","min_ell_then_min_degree_sum","min_boundary_then_min_degree_sum"};
pair<int,int> score(const Row&r,int k){switch(k){case 0:return {r.ell,0};case 1:return {r.ds,0};case 2:return {r.z,0};case 3:return {-r.inherit,0};case 4:return {r.ell,-r.inherit};case 5:return {r.ds,-r.inherit};case 6:return {r.z,-r.inherit};case 7:return {-r.inherit,r.ell};case 8:return {-r.inherit,r.ds};case 9:return {-r.inherit,r.z};case 10:return {r.ell,r.ds};default:return {r.z,r.ds};}}
struct RuleState{pair<int,int> key={INT_MAX,INT_MAX};int best=-1,ties=0,good=0,h0=0,firstH0=-1;};
int main(int argc,char**argv){
 if(argc!=4){cerr<<"usage: miner corpus.txt full_audit_dir output_dir\n";return 2;}
 fs::path audit=argv[2],out=argv[3];fs::create_directories(out);canonical_table();
 map<int,Meta> meta;{ifstream f(audit/"graph_summary.tsv");string line;getline(f,line);while(getline(f,line)){auto v=split(line);meta[stoi(v[0])]={stoi(v[2]),stoi(v[4]),stoi(v[5]),stoi(v[6]),stoi(v[8]),v[1]};}}
 array<Type,1024> types;for(int code=0;code<1024;code++){int a[5]={},bit=0;for(int j=1;j<5;j++)for(int i=0;i<j;i++,bit++)if(code>>bit&1){a[i]|=1<<j;a[j]|=1<<i;}int cc=0,seen=0,lo=5,hi=0;for(int i=0;i<5;i++){lo=min(lo,pc(a[i]));hi=max(hi,pc(a[i]));if(!(seen>>i&1)){cc++;int todo=1<<i;while(todo){int v=__builtin_ctz((unsigned)todo);todo^=1<<v;if(seen>>v&1)continue;seen|=1<<v;todo|=a[v]&~seen;}}}types[code]={pc(code),cc,lo==2&&hi==2,lo,hi};}
 vector<int> numeric,ys;array<int,32768> index{};array<string,32768> names;
 for(int Y=0;Y<32768;Y++)if(pc(Y)==5){index[Y]=numeric.size();numeric.push_back(Y);names[Y]=join(verts(Y));}ys=numeric;sort(ys.begin(),ys.end(),[](int a,int b){return verts(a)<verts(b);});
 vector<string> fn={"fiveset_features.tsv","graph_structure.tsv","rule_evaluations.tsv","canonical_witnesses.tsv","cut_coverage.tsv","category_histograms.tsv"};
 vector<string> headers={
 "graph_id\tgraph6\tY_mask\tY_vertices\tdG\tq\tis_good\tDelta_min\trho\tis_H0_witness\tell\td_GY\te_GY\tboundary_size\tdegree_sum\tmin_degree_in_Y\tmax_degree_in_Y\tinduced_type\tis_independent\tis_C5\tcomponents\tboundary_degree_multiset\tinherited_optimum_count\tglobal_optimum_count\tinherited_optimum_fraction\twitness_f\tmin_induced_degree\tmax_induced_degree",
 "graph_id\tgraph6\tdG\tL\tcritical\toptG_count\tgood_count\tH0_count\tgood_nonH0_count\tbad_count\tmin_cut_good_H0\tmax_cut_good_H0\tbest_f\tone_cut_all_good\tone_cut_all_H0\tH0_inherited_by_all_optima\tH0_independent_or_C5\tH0_types",
 "graph_id\trule\tY_mask\tY_vertices\tscore1\tscore2\tq\tis_good\tis_H0\tDelta_min\trho\tell\tdegree_sum\tboundary_size\tinherited_count\tinduced_type\tprimary_ties\tgood_ties\tH0_ties\tfirst_H0_tie_Y",
 "graph_id\tcriterion\tY_mask\tY_vertices\tf_mask\tq\tell\tdegree_sum\tboundary_size\td_GY\te_GY\tinduced_type\tcomponents\tinherited_count\toptG_count\tmin_degree_in_Y\tmax_degree_in_Y",
 "graph_id\tf_mask\tgood_inherited_count\tgood_total\tH0_union_count\toptG_count",
 "graph_id\tcategory\tfeature\tvalue\tcount"};
 set<int> completed;array<long long,6> offsets{};long long checkpointEnd=0;
 fs::path checkpoint=out/"checkpoints.tsv";
 if(fs::exists(checkpoint)){ifstream c(checkpoint);string line;while(getline(c,line)){istringstream p(line);int id;array<long long,6> z;if(!(p>>id))break;bool ok=true;for(auto&v:z)if(!(p>>v))ok=false;if(!ok)break;completed.insert(id);offsets=z;checkpointEnd+=(long long)line.size()+1;}fs::resize_file(checkpoint,checkpointEnd);}
 array<ofstream,6> streams;
 for(int j=0;j<6;j++){auto path=out/fn[j];if(!completed.empty()){if(!fs::exists(path)||fs::file_size(path)<(uint64_t)offsets[j])throw runtime_error("bad resume file");fs::resize_file(path,offsets[j]);streams[j].open(path,ios::app|ios::binary);}else{if(fs::exists(path)&&fs::file_size(path)>0)throw runtime_error("refusing to overwrite output without checkpoint");streams[j].open(path,ios::binary);streams[j]<<headers[j]<<'\n';}}
 ofstream check(checkpoint,ios::app);ifstream in(argv[1]);Graph g;int dummy;auto start=chrono::steady_clock::now();int done=0;
 const array<string,13> HN={"q","Delta_min","rho","ell","degree_sum","boundary_size","d_GY","e_GY","induced_type","components","min_degree_in_Y","max_degree_in_Y","inherited_count"};
 const array<int,13> CAPS={10,10,6,76,71,51,2,7,1024,6,15,15,43};
 while(in>>g.id>>g.g6>>g.n>>g.m>>dummy){g.es.clear();g.adj.fill(0);for(int j=0;j<g.m;j++){int u,v;in>>u>>v;g.es.push_back({u,v});g.adj[u]|=1<<v;g.adj[v]|=1<<u;}if(completed.count(g.id))continue;if(g.n!=15)throw runtime_error("not n15");auto M=meta.at(g.id);if(M.g6!=g.g6)throw runtime_error("source mismatch");
  string stem=to_string(g.id),s;vector<int> opt;{ifstream f(audit/"checkpoints"/(stem+".opt.txt"));getline(f,s);for(auto x:split(s,','))opt.push_back(stoi(x));}if((int)opt.size()!=M.opt||M.opt>42)throw runtime_error("opt count");
  array<unsigned char,9009> land;{ifstream f(audit/"checkpoints"/(stem+".landscape.bin"),ios::binary);f.read((char*)land.data(),land.size());if(f.gcount()!=9009)throw runtime_error("landscape missing");}
  vector<vector<int>> defects(opt.size());for(int j=0;j<(int)opt.size();j++){for(auto[u,v]:g.es)if((((opt[j]>>u)^(opt[j]>>v))&1)==0)defects[j].push_back((1<<u)|(1<<v));if((int)defects[j].size()!=M.d)throw runtime_error("not optimal source cut");}
  vector<int> percut(opt.size());vector<Row> rr;rr.reserve(3003);array<RuleState,12> rules;array<int,4> canon;canon.fill(-1);int countGood=0,countH0=0,alloptH0=0,simpleH0=0;
  uint32_t hist[3][13][1024]={};string buf;buf.reserve(700000);
  for(int Y:ys){auto vv=verts(Y);int ix=index[Y],dH=land[3*ix];Row r{};r.Y=Y;r.q=M.d-dH;r.dm=land[3*ix+1];r.rho=land[3*ix+2];r.good=r.q<=5;r.lo=15;r.wf=-1;int code=0,bit=0,ds=0,lo=15,hi=0;array<int,5> bd;
   for(int j=0;j<5;j++){int d=pc(g.adj[vv[j]]),di=pc(g.adj[vv[j]]&Y);ds+=d;lo=min(lo,d);hi=max(hi,d);bd[j]=d-di;}
   for(int j=1;j<5;j++)for(int i=0;i<j;i++,bit++)code|=((g.adj[vv[i]]>>vv[j])&1)<<bit;
   auto t=types[code];r.ds=ds;r.lo=lo;r.hi=hi;r.ey=t.edges;r.dy=t.dy;r.z=ds-2*r.ey;r.ell=r.z+2*r.dy;r.type=canon5[code];r.comp=t.comp;r.ilo=t.lo;r.ihi=t.hi;
   int md=99;for(int j=0;j<(int)opt.size();j++){int monoH=0;for(int e:defects[j])monoH+=(e&Y)==0;int delta=monoH-dH;if(delta<0)throw runtime_error("negative Delta");md=min(md,delta);if(!delta){r.inherit++;if(r.wf<0)r.wf=opt[j];if(r.good)percut[j]++;}}
   if(md!=r.dm||(r.inherit>0)!=(r.rho==0)||(r.inherit>0)!=(r.dm==0))throw runtime_error("inherited audit disagreement");r.h0=r.good&&r.inherit>0;countGood+=r.good;countH0+=r.h0;alloptH0+=r.h0&&r.inherit==M.opt;simpleH0+=r.h0&&(r.ey==0||r.dy==1);
   int row=rr.size();rr.push_back(r);for(int k=0;k<12;k++){auto key=score(r,k);auto &a=rules[k];if(key<a.key){a.key=key;a.best=row;a.ties=1;a.good=r.good;a.h0=r.h0;a.firstH0=r.h0?Y:-1;}else if(key==a.key){a.ties++;a.good+=r.good;a.h0+=r.h0;if(a.firstH0<0&&r.h0)a.firstH0=Y;}}
   if(r.h0){array<int,4> val={r.ell,r.ds,r.z,0};for(int k=0;k<4;k++){if(canon[k]<0){canon[k]=row;continue;}auto a=rr[canon[k]];array<int,4> av={a.ell,a.ds,a.z,0};if(val[k]<av[k])canon[k]=row;}}
   int category=r.h0?0:r.good?1:2;array<int,13> hv={r.q,r.dm,r.rho,r.ell,r.ds,r.z,r.dy,r.ey,r.type,r.comp,r.lo,r.hi,r.inherit};for(int j=0;j<13;j++){if(hv[j]<0||hv[j]>=CAPS[j])throw runtime_error("feature range");hist[category][j][hv[j]]++;}
   put(buf,g.id);buf+=g.g6;buf+='\t';put(buf,Y);buf+=names[Y];buf+='\t';for(int v:{M.d,r.q,int(r.good),r.dm,r.rho,int(r.h0),r.ell,r.dy,r.ey,r.z,r.ds,r.lo,r.hi,r.type,int(r.ey==0),r.dy,r.comp})put(buf,v);
   sort(bd.begin(),bd.end());for(int j=0;j<5;j++){char b[16];auto z=to_chars(b,b+16,bd[j]);buf.append(b,z.ptr);buf+=j==4?'\t':',';}
   put(buf,r.inherit);put(buf,M.opt);{char b[32];auto a=to_chars(b,b+32,r.inherit);buf.append(b,a.ptr);buf+='/';a=to_chars(b,b+32,M.opt);buf.append(b,a.ptr);buf+='\t';}put(buf,r.h0?r.wf:-1);put(buf,r.ilo);put(buf,r.ihi,false);
  }
  if(countGood!=M.good||!countH0)throw runtime_error("prior H0 audit mismatch");streams[0].write(buf.data(),buf.size());
  int mx=*max_element(percut.begin(),percut.end()),mn=*min_element(percut.begin(),percut.end()),bestf=opt[max_element(percut.begin(),percut.end())-percut.begin()];vector<int>h0types;for(int x=0;x<1024;x++)if(hist[0][8][x])h0types.push_back(x);
  streams[1]<<g.id<<'\t'<<g.g6<<'\t'<<M.d<<'\t'<<M.L<<'\t'<<M.crit<<'\t'<<M.opt<<'\t'<<countGood<<'\t'<<countH0<<'\t'<<countGood-countH0<<'\t'<<3003-countGood<<'\t'<<mn<<'\t'<<mx<<'\t'<<bestf<<'\t'<<(mx==countGood)<<'\t'<<(mx==countH0)<<'\t'<<alloptH0<<'\t'<<simpleH0<<'\t'<<join(h0types)<<'\n';
  for(int k=0;k<12;k++){auto a=rules[k];auto r=rr[a.best];streams[2]<<g.id<<'\t'<<RULES[k]<<'\t'<<r.Y<<'\t'<<names[r.Y]<<'\t'<<a.key.first<<'\t'<<a.key.second<<'\t'<<r.q<<'\t'<<r.good<<'\t'<<r.h0<<'\t'<<r.dm<<'\t'<<r.rho<<'\t'<<r.ell<<'\t'<<r.ds<<'\t'<<r.z<<'\t'<<r.inherit<<'\t'<<r.type<<'\t'<<a.ties<<'\t'<<a.good<<'\t'<<a.h0<<'\t'<<a.firstH0<<'\n';}
  const array<string,4>cn={"min_ell","min_degree_sum","min_boundary","lex_vertices"};for(int k=0;k<4;k++){auto r=rr[canon[k]];streams[3]<<g.id<<'\t'<<cn[k]<<'\t'<<r.Y<<'\t'<<names[r.Y]<<'\t'<<r.wf<<'\t'<<r.q<<'\t'<<r.ell<<'\t'<<r.ds<<'\t'<<r.z<<'\t'<<r.dy<<'\t'<<r.ey<<'\t'<<r.type<<'\t'<<r.comp<<'\t'<<r.inherit<<'\t'<<M.opt<<'\t'<<r.lo<<'\t'<<r.hi<<'\n';}
  for(int j=0;j<(int)opt.size();j++)streams[4]<<g.id<<'\t'<<opt[j]<<'\t'<<percut[j]<<'\t'<<countGood<<'\t'<<countH0<<'\t'<<M.opt<<'\n';
  const array<string,3>cats={"H0","good_nonH0","bad"};for(int c=0;c<3;c++)for(int j=0;j<13;j++)for(int v=0;v<CAPS[j];v++)if(hist[c][j][v])streams[5]<<g.id<<'\t'<<cats[c]<<'\t'<<HN[j]<<'\t'<<v<<'\t'<<hist[c][j][v]<<'\n';
  for(int j=0;j<6;j++){streams[j].flush();if(!streams[j])throw runtime_error("write failure");offsets[j]=streams[j].tellp();}check<<g.id;for(auto p:offsets)check<<'\t'<<p;check<<'\n';check.flush();if(!check)throw runtime_error("checkpoint write");
  done++;ostringstream progress;progress<<"completed id="<<g.id<<" H0="<<countH0<<" max_cut_good="<<mx<<" good="<<countGood<<" processed="<<done<<" elapsed="<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"s\n";cerr<<progress.str();
 }
 cerr<<"COMPLETE newly processed="<<done<<"\n";
}
