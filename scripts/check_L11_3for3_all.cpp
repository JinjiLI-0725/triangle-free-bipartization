#include <bits/stdc++.h>
using namespace std;

struct Graph {
    int n;
    vector<pair<int,int>> edges;
};

static int maxcut(const Graph& G) {
    if (G.n <= 1) return 0;

    int best = 0;

    // Fix vertex 0 to side 0, eliminating global complement symmetry.
    const int lim = 1 << (G.n - 1);

    for (int mask = 0; mask < lim; ++mask) {
        int cut = 0;

        for (auto [u,v] : G.edges) {
            int cu = (u == 0 ? 0 : ((mask >> (u-1)) & 1));
            int cv = (v == 0 ? 0 : ((mask >> (v-1)) & 1));
            cut += (cu != cv);
        }

        best = max(best, cut);
    }

    return best;
}

static int deletion_distance(const Graph& G) {
    return (int)G.edges.size() - maxcut(G);
}

static Graph delete_vertices(
    const Graph& G,
    const array<int,5>& Y
) {
    vector<char> del(G.n, false);

    for (int v : Y) {
        if (v < 0 || v >= G.n) {
            throw runtime_error("vertex out of range");
        }
        del[v] = true;
    }

    vector<int> mp(G.n, -1);
    int next = 0;

    for (int v = 0; v < G.n; ++v) {
        if (!del[v]) mp[v] = next++;
    }

    Graph H;
    H.n = next;

    for (auto [u,v] : G.edges) {
        if (!del[u] && !del[v]) {
            H.edges.push_back({mp[u], mp[v]});
        }
    }

    return H;
}

static bool triangle_free(const Graph& G) {
    vector<vector<char>> A(G.n, vector<char>(G.n, false));

    for (auto [u,v] : G.edges)
        A[u][v] = A[v][u] = true;

    for (int a = 0; a < G.n; ++a)
    for (int b = a+1; b < G.n; ++b)
    for (int c = b+1; c < G.n; ++c) {
        if (A[a][b] && A[a][c] && A[b][c])
            return false;
    }

    return true;
}

int main(int argc, char** argv) {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (argc != 3) {
        cerr
            << "usage: " << argv[0]
            << " <input.txt> <output.tsv>\n";
        return 2;
    }

    ifstream fin(argv[1]);
    if (!fin) {
        cerr << "cannot open input: " << argv[1] << "\n";
        return 2;
    }

    ofstream fout(argv[2]);
    if (!fout) {
        cerr << "cannot open output: " << argv[2] << "\n";
        return 2;
    }

    int T;
    fin >> T;

    fout
        << "id\tdG\tpass\tq_found\tY\t"
        << "explicit_search\n";

    int passed = 0;
    int failed = 0;
    long long explicit_checks = 0;
    int nontrivial = 0;

    map<int,int> d_distribution;
    map<int,int> q_distribution_nontrivial;
    vector<int> failures;

    for (int tc = 0; tc < T; ++tc) {
        int id, dG, m;

        array<int,5> X{};

        fin >> id >> dG;

        for (int &x : X)
            fin >> x;

        fin >> m;

        Graph G;
        G.n = 15;
        G.edges.resize(m);

        for (auto &[u,v] : G.edges)
            fin >> u >> v;

        if (!triangle_free(G)) {
            cerr
                << "ERROR: input graph is not triangle-free; id="
                << id << "\n";
            return 3;
        }

        // Independently re-check the stored exact d(G).
        const int exact_dG = deletion_distance(G);

        if (exact_dG != dG) {
            cerr
                << "ERROR: d(G) mismatch for id=" << id
                << " stored=" << dG
                << " exact=" << exact_dG
                << "\n";
            return 4;
        }

        d_distribution[dG]++;

        bool inX[15] = {};
        for (int x : X)
            inX[x] = true;

        vector<int> outside;
        for (int v = 0; v < 15; ++v)
            if (!inX[v])
                outside.push_back(v);

        if (outside.size() != 10) {
            cerr
                << "ERROR: distinguished X invalid for id="
                << id << "\n";
            return 5;
        }

        bool ok = false;
        bool explicit_search = (dG > 5);
        int q_found = INT_MAX;
        array<int,5> Y_found{};

        // If d(G) <= 5, every deletion set automatically satisfies
        // q(Y) = d(G)-d(G-Y) <= d(G) <= 5.
        if (!explicit_search) {
            Y_found = {
                X[0], X[1],
                outside[0], outside[1], outside[2]
            };

            Graph H = delete_vertices(G, Y_found);
            q_found = dG - deletion_distance(H);

            if (q_found > 5) {
                cerr
                    << "ERROR: automatic case failed id="
                    << id << "\n";
                return 6;
            }

            ok = true;
        } else {
            ++nontrivial;

            // Exactly 2 vertices from X and exactly 3 from V(G)\X.
            for (int a = 0; a < 5 && !ok; ++a)
            for (int b = a+1; b < 5 && !ok; ++b)
            for (int i = 0; i < 10 && !ok; ++i)
            for (int j = i+1; j < 10 && !ok; ++j)
            for (int k = j+1; k < 10 && !ok; ++k) {

                array<int,5> Y = {
                    X[a], X[b],
                    outside[i], outside[j], outside[k]
                };

                Graph H = delete_vertices(G, Y);

                int q = dG - deletion_distance(H);
                ++explicit_checks;

                if (q <= 5) {
                    ok = true;
                    q_found = q;
                    Y_found = Y;
                }
            }

            if (ok)
                q_distribution_nontrivial[q_found]++;
        }

        if (ok)
            ++passed;
        else {
            ++failed;
            failures.push_back(id);
        }

        fout
            << id << '\t'
            << dG << '\t'
            << (ok ? 1 : 0) << '\t'
            << (ok ? q_found : -1) << '\t';

        if (ok) {
            fout
                << Y_found[0] << ","
                << Y_found[1] << ","
                << Y_found[2] << ","
                << Y_found[3] << ","
                << Y_found[4];
        }

        fout
            << '\t'
            << (explicit_search ? 1 : 0)
            << '\n';
    }

    cout << "classes=" << T << "\n";
    cout << "passed=" << passed << "\n";
    cout << "failed=" << failed << "\n";
    cout << "all_3for3_pass="
         << (failed == 0 ? "true" : "false")
         << "\n";

    cout << "nontrivial_dG_gt_5="
         << nontrivial << "\n";

    cout << "explicit_Y_checks="
         << explicit_checks << "\n";

    cout << "dG_distribution=";
    for (auto [d,n] : d_distribution)
        cout << " d" << d << ":" << n;
    cout << "\n";

    cout << "first_success_q_distribution_nontrivial=";
    for (auto [q,n] : q_distribution_nontrivial)
        cout << " q" << q << ":" << n;
    cout << "\n";

    if (!failures.empty()) {
        cout << "failed_ids=";
        for (int id : failures)
            cout << " " << id;
        cout << "\n";
    }

    return failed == 0 ? 0 : 1;
}
