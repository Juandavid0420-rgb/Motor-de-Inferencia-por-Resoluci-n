# archivo: resolucion_primer_orden.py
# -------------------------------------------------
# Resolución en Lógica de Primer Orden con UNIFICACIÓN (Robinson)
# -------------------------------------------------
# PROPÓSITO DEL ARCHIVO
# - Implementar un motor de resolución por refutación en Lógica de Primer Orden.
# - Incluir unificador de Robinson con occurs-check (evita x = f(x)).
# - Trabajar sobre cláusulas YA en CNF (Forma Normal Conjuntiva) para mantener el foco en unificación + resolución.
#
# CÓMO SE USA (resumen):
# 1) Define la Base de Conocimiento (KB) como un conjunto de cláusulas (cada cláusula es un conjunto de literales).
# 2) Define la meta (conclusión que deseas probar) y agrega su negación como "meta_negada" (otra cláusula).
# 3) Llama a resolucion_primer_orden(KB, meta_negada). Si aparece la cláusula vacía => éxito.
#
# DISEÑO (mapa rápido):
# - Modelado de Términos: Variable, Constante, Funcion.
# - Predicados y Literales: predicado(nombre, args), literal(negado=True/False).
# - Sustituciones: dict de Variable -> Término; se aplican recursivamente a términos/literales/cláusulas.
# - Unificación (unificar): construye la sustitución más general (MGU) o falla.
# - Resolución: busca pares de literales complementarios entre dos cláusulas, unifica, aplica sustitución y arma resolvente.

from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set, FrozenSet, Optional, Union

# -----------------------------
# 1) Estructuras de datos (representación lógica)
# -----------------------------
# Estas clases permiten representar términos y fórmulas de primer orden de forma tipada y clara.

@dataclass(frozen=True)
class Variable:
    nombre: str  # Identificador de la variable, p.ej. 'x', 'y'
    def __str__(self) -> str:
        return self.nombre

@dataclass(frozen=True)
class Constante:
    nombre: str  # Constante simbólica, p.ej. 'Socrates', 'Ana'
    def __str__(self) -> str:
        return self.nombre

@dataclass(frozen=True)
class Funcion:
    simbolo: str                  # Nombre de la función, p.ej. 'padreDe', 'f'
    argumentos: Tuple['Termino', ...]  # Tupla de términos como argumentos
    def __str__(self) -> str:
        return f"{self.simbolo}({', '.join(map(str, self.argumentos))})"

# Un término puede ser una Variable, una Constante o una Funcion
Termino = Union[Variable, Constante, Funcion]

@dataclass(frozen=True)
class Predicado:
    nombre: str                  # Nombre del predicado, p.ej. 'Humano', 'Mortal', 'Padre'
    argumentos: Tuple[Termino, ...]  # Argumentos (términos)
    def __str__(self) -> str:
        return f"{self.nombre}({', '.join(map(str, self.argumentos))})"

@dataclass(frozen=True)
class Literal:
    predicado: Predicado         # Predicado con sus argumentos
    negado: bool = False         # True si es ¬Predicado(...)
    def __str__(self) -> str:
        return ("¬" if self.negado else "") + str(self.predicado)

# Alias semánticos
Clausula = FrozenSet[Literal]               # Disyunción de literales
Sustitucion = Dict[Variable, Termino]       # Mapeo Variable -> Termino

# -----------------------------
# 2) Sustituciones y occurs-check (utilidades)
# -----------------------------
# Las sustituciones se aplican recursivamente. El occurs-check impide ciclos del tipo x = f(x).

def aplicar_sustitucion_termino(termino: Termino, sustitucion: Sustitucion) -> Termino:
    """Aplica una sustitución a un término (de forma recursiva si es una función)."""
    # Si el término es una variable con sustitución, la expandimos hasta alcanzar un término base
    if isinstance(termino, Variable) and termino in sustitucion:
        return aplicar_sustitucion_termino(sustitucion[termino], sustitucion)
    # Si es función, aplicamos en cada argumento
    if isinstance(termino, Funcion):
        return Funcion(termino.simbolo, tuple(aplicar_sustitucion_termino(t, sustitucion) for t in termino.argumentos))
    # Constante o variable sin sustitución
    return termino


def ocurre_en(variable: Variable, termino: Termino, sustitucion: Sustitucion) -> bool:
    """Devuelve True si 'variable' ocurre dentro de 'termino' bajo la sustitución (occurs-check)."""
    termino = aplicar_sustitucion_termino(termino, sustitucion)
    if isinstance(termino, Variable):
        return termino == variable
    if isinstance(termino, Funcion):
        return any(ocurre_en(variable, arg, sustitucion) for arg in termino.argumentos)
    return False


def aplicar_sustitucion_literal(lit: Literal, sustitucion: Sustitucion) -> Literal:
    """Aplica una sustitución a TODOS los argumentos del literal."""
    nuevos_argumentos = tuple(aplicar_sustitucion_termino(a, sustitucion) for a in lit.predicado.argumentos)
    return Literal(Predicado(lit.predicado.nombre, nuevos_argumentos), lit.negado)


def aplicar_sustitucion_clausula(clausula: Clausula, sustitucion: Sustitucion) -> Clausula:
    """Aplica una sustitución a cada literal de una cláusula."""
    return frozenset(aplicar_sustitucion_literal(l, sustitucion) for l in clausula)

# -----------------------------
# 3) Unificación (Robinson)
# -----------------------------
# Idea: encontrar la Sustitución Más General (SMG/MGU) que hace iguales dos términos.
# Casos:
# - Variables: se pueden ligar a términos si no violan occurs-check.
# - Funciones: mismo símbolo y misma aridad; unificar argumento a argumento.
# - Constantes: deben ser idénticas.

def unificar(t1: Termino, t2: Termino, s: Optional[Sustitucion] = None) -> Optional[Sustitucion]:
    """Devuelve la sustitución más general que unifica t1 y t2, o None si falla."""
    if s is None:
        s = {}
    # Siempre comparamos términos ya bajo la sustitución acumulada
    t1 = aplicar_sustitucion_termino(t1, s)
    t2 = aplicar_sustitucion_termino(t2, s)

    # Caso base: ya son iguales
    if t1 == t2:
        return s

    # Caso variable (puede ligarse si no hay ciclo)
    if isinstance(t1, Variable):
        if ocurre_en(t1, t2, s):
            return None
        s = s.copy(); s[t1] = t2
        return s
    if isinstance(t2, Variable):
        if ocurre_en(t2, t1, s):
            return None
        s = s.copy(); s[t2] = t1
        return s

    # Caso función: mismo símbolo y aridad, unificar argumento a argumento
    if isinstance(t1, Funcion) and isinstance(t2, Funcion) and t1.simbolo == t2.simbolo and len(t1.argumentos) == len(t2.argumentos):
        for a, b in zip(t1.argumentos, t2.argumentos):
            s = unificar(a, b, s)
            if s is None:
                return None
        return s

    # Constantes distintas o funciones incompatibles
    return None


def unificar_literales(lit_a: Literal, lit_b: Literal) -> Optional[Sustitucion]:
    """Intenta unificar dos literales con signos complementarios (uno negado y el otro no)."""
    # Deben tener el MISMO predicado (nombre) y la MISMA aridad
    if lit_a.predicado.nombre != lit_b.predicado.nombre:
        return None
    if len(lit_a.predicado.argumentos) != len(lit_b.predicado.argumentos):
        return None
    # Deben ser complementarios en el signo: L y ¬L
    if lit_a.negado == lit_b.negado:
        return None

    # Unificamos argumentos en orden; si algo falla, devolvemos None
    s: Sustitucion = {}
    for arg_a, arg_b in zip(lit_a.predicado.argumentos, lit_b.predicado.argumentos):
        s = unificar(arg_a, arg_b, s)
        if s is None:
            return None
    return s

# -----------------------------
# 4) Resolución en Primer Orden
# -----------------------------
# Dadas dos cláusulas, busca pares de literales complementarios que unifican,
# aplica la sustitución resultante y construye el resolvente (uniendo el resto de literales).
# Descarta resolventes tautológicos (si contienen un literal y su negación simultáneamente).

def obtener_resolventes(clausula_a: Clausula, clausula_b: Clausula) -> List[Clausula]:
    """Calcula todos los resolventes entre dos cláusulas aplicando unificación entre literales complementarios."""
    lista_resolventes: List[Clausula] = []
    for lit_a in clausula_a:
        for lit_b in clausula_b:
            sustitucion = unificar_literales(lit_a, lit_b)
            if sustitucion is None:
                continue
            # Construir el resolvente aplicando la sustitución a las partes restantes
            nueva_a = aplicar_sustitucion_clausula(clausula_a - {lit_a}, sustitucion)
            nueva_b = aplicar_sustitucion_clausula(clausula_b - {lit_b}, sustitucion)
            resolvente = frozenset(nueva_a | nueva_b)
            # Evitar tautologías: literal y su negación dentro de la misma cláusula
            if any(L1.negado != L2.negado and L1.predicado == L2.predicado for L1 in resolvente for L2 in resolvente):
                continue
            lista_resolventes.append(resolvente)
    return lista_resolventes


def resolucion_primer_orden(base_conocimiento: Set[Clausula], meta_negada: Clausula, max_iteraciones: int = 500) -> Tuple[bool, List[Tuple[Clausula, Clausula, Clausula]]]:
    """Bucle principal de resolución por refutación en Primer Orden.
    - base_conocimiento: conjunto de cláusulas en CNF.
    - meta_negada: cláusula con la negación de la conclusión buscada.
    - max_iteraciones: tope para evitar bucles largos.

    Retorna (exito, traza) donde 'traza' lista triples (c1, c2, resolvente).
    """
    # Conjunto de trabajo inicial S = KB ∪ {meta_negada}
    conjunto_trabajo: Set[Clausula] = set(base_conocimiento)
    conjunto_trabajo.add(meta_negada)

    traza: List[Tuple[Clausula, Clausula, Clausula]] = []  # Para explicar cada paso en consola
    nuevos: Set[Clausula] = set()                           # Resolventes generados en cada iteración

    for _ in range(max_iteraciones):
        lista = list(conjunto_trabajo)
        for i in range(len(lista)):
            for j in range(i + 1, len(lista)):
                c1, c2 = lista[i], lista[j]
                for resolvente in obtener_resolventes(c1, c2):
                    traza.append((c1, c2, resolvente))
                    if len(resolvente) == 0:  # cláusula vacía => éxito
                        return True, traza
                    nuevos.add(resolvente)
        # Si no hay progreso, detenemos la búsqueda
        if nuevos.issubset(conjunto_trabajo):
            return False, traza
        # Agregamos los resolventes nuevos y repetimos
        conjunto_trabajo |= nuevos
        nuevos.clear()

    # Alcanzado el tope sin derivar la cláusula vacía
    return False, traza

# -----------------------------
# 5) Ejemplo de uso: "Sócrates es mortal"
# -----------------------------
# KB:
#   1) ¬Humano(x) ∨ Mortal(x)
#   2) Humano(Socrates)
# Objetivo: Mortal(Socrates)
# Refutación: agregar ¬Mortal(Socrates) como meta_negada
if __name__ == "__main__":
    # Variables y constantes de ejemplo
    x = Variable('x')
    Socrates = Constante('Socrates')

    # Predicados/literales auxiliares (lambdas para escribir más limpio)
    Humano    = lambda t: Literal(Predicado('Humano', (t,)))
    noHumano  = lambda t: Literal(Predicado('Humano', (t,)), negado=True)
    Mortal    = lambda t: Literal(Predicado('Mortal', (t,)))
    noMortal  = lambda t: Literal(Predicado('Mortal', (t,)), negado=True)

    # Cláusulas de la KB en CNF
    clausula1: Clausula = frozenset({ noHumano(x), Mortal(x) })     # ¬Humano(x) ∨ Mortal(x)
    clausula2: Clausula = frozenset({ Humano(Socrates) })           # Humano(Socrates)
    base: Set[Clausula] = { clausula1, clausula2 }

    # Negación de la conclusión
    meta_negada: Clausula = frozenset({ noMortal(Socrates) })       # ¬Mortal(Socrates)

    # Ejecutar resolución
    exito, traza = resolucion_primer_orden(base, meta_negada)
    print("¿Se derivó la cláusula vacía?", exito)

    # Imprimir traza legible: muestra padres y resolvente en cada paso
    for origen_a, origen_b, resolvente in traza:
        imprime_a = { str(elem) for elem in origen_a }
        imprime_b = { str(elem) for elem in origen_b }
        imprime_r = { str(elem) for elem in resolvente }
        print(f"{imprime_a} RES {imprime_b}  =>  {imprime_r}")