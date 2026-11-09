#include <bits/stdc++.h>
using namespace std;

struct ArbolTimestamps {
    int n;
    int reloj = 0;
    vector<vector<int>> ady;
    vector<int> tin, tout, padre;
    vector<array<int, 3>> eventos;
    vector<pair<int, int>> aristas;

    explicit ArbolTimestamps(int n_)
        : n(n_), ady(n_ + 1), tin(n_ + 1, 0), tout(n_ + 1, 0), padre(n_ + 1, 0) {}

    void agregar_arista(int u, int v) {
        ady[u].push_back(v);
        ady[v].push_back(u);
        aristas.push_back({u, v});
    }

    void dfs(int raiz) {
        vector<int> siguiente(n + 1, 0);
        vector<int> pila;

        padre[raiz] = 0;
        tin[raiz] = ++reloj;
        eventos.push_back({0, raiz, tin[raiz]});
        pila.push_back(raiz);

        while (!pila.empty()) {
            int u = pila.back();
            if (siguiente[u] < (int)ady[u].size()) {
                int v = ady[u][siguiente[u]++];
                if (v == padre[u]) continue;
                padre[v] = u;
                tin[v] = ++reloj;
                eventos.push_back({0, v, tin[v]});
                pila.push_back(v);
            } else {
                tout[u] = ++reloj;
                eventos.push_back({1, u, tout[u]});
                pila.pop_back();
            }
        }
    }

    bool es_ancestro(int u, int v) const {
        return tin[u] <= tin[v] && tout[v] <= tout[u];
    }

    int tam_subarbol(int v) const {
        return (tout[v] - tin[v] + 1) / 2;
    }
};

int main(int argc, char** argv) {
    bool modo_traza = (argc > 1 && string(argv[1]) == "--trace");
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    if (!(cin >> n >> q) || n < 1) {
        cerr << "entrada invalida: se esperaba \"n q\" con n >= 1\n";
        return 1;
    }
    ArbolTimestamps arbol(n);
    for (int i = 1; i < n; ++i) {
        int u, v;
        cin >> u >> v;
        arbol.agregar_arista(u, v);
    }
    arbol.dfs(1);

    if (!modo_traza) {
        while (q--) {
            int u, v;
            cin >> u >> v;
            cout << (arbol.es_ancestro(u, v) ? "SI" : "NO") << '\n';
        }
        return 0;
    }

    cout << "{\"n\":" << n << ",\"edges\":[";
    for (size_t i = 0; i < arbol.aristas.size(); ++i)
        cout << (i ? "," : "") << "[" << arbol.aristas[i].first << "," << arbol.aristas[i].second << "]";
    cout << "],\"events\":[";
    for (size_t i = 0; i < arbol.eventos.size(); ++i) {
        const auto& e = arbol.eventos[i];
        cout << (i ? "," : "") << "{\"type\":\"" << (e[0] ? "exit" : "enter")
             << "\",\"u\":" << e[1] << ",\"t\":" << e[2] << "}";
    }
    cout << "],\"queries\":[";
    for (int i = 0; i < q; ++i) {
        int u, v;
        cin >> u >> v;
        cout << (i ? "," : "") << "{\"u\":" << u << ",\"v\":" << v
             << ",\"result\":" << (arbol.es_ancestro(u, v) ? "true" : "false") << "}";
    }
    cout << "]}\n";
    return 0;
}