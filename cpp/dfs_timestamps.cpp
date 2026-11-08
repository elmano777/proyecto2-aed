// DFS Timestamps (tin / tout)
// Base: código de clase del Prof. Víctor Racsó Galván Oyola (CS2023, UTEC).
// Adaptación del grupo: modo --trace, que además de resolver las consultas emite
// una traza JSON (eventos enter/exit del DFS) que consume la animación en Manim.
//
//   ./dfs_timestamps          -> imprime SI/NO por consulta (comportamiento original)
//   ./dfs_timestamps --trace  -> imprime la traza JSON para la animación
//
// Entrada: "n q", luego n-1 aristas "u v", luego q consultas "u v" (nodos 1..n, raíz 1).
#include<bits/stdc++.h>
using namespace::std;

const int N = 200000 + 5;

int T;
int in[N];
int out[N];
vector<int> G[N];

// --- agregado por el grupo: registro de eventos para la animación ---
vector<array<int,3>> eventos;          // {0 = enter / 1 = exit, nodo, tiempo}
vector<pair<int,int>> aristas;
// ---------------------------------------------------------------------

void add_edge(int u, int v) {
    G[u].emplace_back(v);
    G[v].emplace_back(u);
    aristas.push_back({u, v});
}

void DFS(int u, int p = -1) {
    in[u] = ++T;
    eventos.push_back({0, u, in[u]});
    for (int &v : G[u]) {
        if (v == p) continue;
        DFS(v, u);
    }
    out[u] = ++T;
    eventos.push_back({1, u, out[u]});
}

bool is_ancestor(int u, int v) {
    return in[u] <= in[v] and out[v] <= out[u];
}

int main(int argc, char** argv) {
    bool trace = (argc > 1 && string(argv[1]) == "--trace");
    cin.tie(0) -> sync_with_stdio(false);
    int n, q;
    cin >> n >> q;
    for (int i = 1; i < n; ++i) {
        int u, v;
        cin >> u >> v;
        add_edge(u, v);
    }
    DFS(1); // DFS desde la raiz

    if (!trace) {
        while (q--) {
            int u, v;
            cin >> u >> v;
            cout << (is_ancestor(u, v) ? "SI" : "NO") << '\n';
        }
        return 0;
    }

    // --- modo traza (agregado por el grupo) ---
    cout << "{\"n\":" << n << ",\"edges\":[";
    for (size_t i = 0; i < aristas.size(); ++i)
        cout << (i ? "," : "") << "[" << aristas[i].first << "," << aristas[i].second << "]";
    cout << "],\"events\":[";
    for (size_t i = 0; i < eventos.size(); ++i)
        cout << (i ? "," : "") << "{\"type\":\"" << (eventos[i][0] ? "exit" : "enter")
             << "\",\"u\":" << eventos[i][1] << ",\"t\":" << eventos[i][2] << "}";
    cout << "],\"queries\":[";
    for (int i = 0; i < q; ++i) {
        int u, v;
        cin >> u >> v;
        cout << (i ? "," : "") << "{\"u\":" << u << ",\"v\":" << v
             << ",\"result\":" << (is_ancestor(u, v) ? "true" : "false") << "}";
    }
    cout << "]}\n";
    return 0;
}
