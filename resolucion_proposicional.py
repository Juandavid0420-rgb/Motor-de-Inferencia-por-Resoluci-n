# archivo: resolucion_proposicional.py
# ------------------------------------
# Motor de resolución proposicional por refutación

from typing import FrozenSet, Set, Tuple, List

# Definiciones de tipos 
Literal = str                 # Ejemplos: "p", "q", "~p" ("~" representa la negación)
Clausula = FrozenSet[Literal] # Una cláusula es una disyunción (OR) de literales


def negar_literal(literal: Literal) -> Literal:
    """Devuelve la negación de un literal: p -> ~p, ~p -> p."""
    return literal[1:] if literal.startswith('~') else '~' + literal


def resolver_pareja(clausula_a: Clausula, clausula_b: Clausula) -> List[Clausula]:
    """Genera todos los resolventes posibles entre dos cláusulas proposicionales.
    Idea: si en A está L y en B está ~L, el resolvente es (A − {L}) ∪ (B − {~L}).
    Se descartan tautologías (cláusulas que contienen a la vez L y ~L).
    """
    lista_resolventes: List[Clausula] = []
    for literal in clausula_a:
        literal_negado = negar_literal(literal)
        if literal_negado in clausula_b:
            nueva_clausula = frozenset((clausula_a - {literal}) | (clausula_b - {literal_negado}))
            # Evitar tautologías: si contiene un literal y su negación, no aporta información
            if any(negar_literal(x) in nueva_clausula for x in nueva_clausula):
                continue
            lista_resolventes.append(nueva_clausula)
    return lista_resolventes


def resolucion_por_refutacion(base_conocimiento: Set[Clausula], meta_negada: Clausula) -> Tuple[bool, List[Tuple[Clausula, Clausula, Clausula]]]:
    """Aplica resolución por refutación: (KB ∧ meta_negada) ⟶ deriva cláusula vacía?
    Retorna (exito, traza). La traza registra cada par de cláusulas y su resolvente.
    """
    conjunto_trabajo: Set[Clausula] = set(base_conocimiento)
    conjunto_trabajo.add(meta_negada)
    nuevo_conjunto: Set[Clausula] = set()
    traza: List[Tuple[Clausula, Clausula, Clausula]] = []

    while True:
        lista_clausulas = list(conjunto_trabajo)
        total = len(lista_clausulas)
        for i in range(total):
            for j in range(i + 1, total):
                c1, c2 = lista_clausulas[i], lista_clausulas[j]
                for resolvente in resolver_pareja(c1, c2):
                    traza.append((c1, c2, resolvente))
                    if len(resolvente) == 0:  # cláusula vacía (éxito)
                        return True, traza
                    nuevo_conjunto.add(resolvente)
        # Si no hay progreso, se detiene
        if nuevo_conjunto.issubset(conjunto_trabajo):
            return False, traza
        conjunto_trabajo |= nuevo_conjunto
        nuevo_conjunto.clear()


if __name__ == "__main__":
    # Ejemplo para sustentar:
    # KB = { (p ∨ q), (~p ∨ r), (~q ∨ r) }
    # Queremos demostrar r. Por refutación agregamos ~r como meta_negada.
    KB: Set[Clausula] = {
        frozenset({"p", "q"}),
        frozenset({"~p", "r"}),
        frozenset({"~q", "r"})
    }
    meta_negada: Clausula = frozenset({"~r"})

    exito, traza_resolucion = resolucion_por_refutacion(KB, meta_negada)
    print("¿Se derivó la cláusula vacía?", exito)
    for c1, c2, resolvente in traza_resolucion:
        print(f"{set(c1)} RES {set(c2)}  =>  {set(resolvente)}")