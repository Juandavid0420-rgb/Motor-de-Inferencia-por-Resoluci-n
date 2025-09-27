# Proyecto 2 — Motor de Inferencia por Resolución (Python)

## 📌 Descripción

Este proyecto implementa un **motor de inferencia basado en resolución por refutación**, en dos etapas:

1. **Resolución Proposicional** (sin variables): trabaja únicamente con literales proposicionales.
2. **Resolución en Primer Orden** (con unificación de variables): incluye el algoritmo de **unificación de Robinson** y aplica resolución sobre cláusulas en **Forma Normal Conjuntiva (CNF)**.

El objetivo es demostrar teoremas mediante **refutación**: se añade la negación de la conclusión a la base de conocimiento (KB) y se intenta derivar la **cláusula vacía (⊥)**.

---

## 📂 Archivos principales

* `resolucion_proposicional.py` → Motor proposicional con variables simples (p, q, r...).
* `resolucion_primer_orden.py` → Motor de primer orden con variables, constantes y unificación.

---

## ⚙️ Requisitos

* Python 3.8 o superior.

No se necesitan librerías externas (solo `dataclasses` y `typing`).

---

## ▶️ Ejecución

### 1. Resolución proposicional

```bash
python3 resolucion_proposicional.py
```

**Ejemplo implementado:**

* KB = { (p ∨ q), (¬p ∨ r), (¬q ∨ r) }
* Conclusión: r
* Se agrega ¬r como meta negada.
* Resultado: derivación de la cláusula vacía ⇒ `r` es consecuencia lógica de KB.

### 2. Resolución de primer orden

```bash
python3 resolucion_primer_orden.py
```

**Ejemplo implementado:**

* KB:

  1. ¬Humano(x) ∨ Mortal(x)
  2. Humano(Socrates)
* Conclusión: Mortal(Socrates)
* Se agrega ¬Mortal(Socrates) como meta negada.
* Resultado: se deriva la cláusula vacía ⇒ Sócrates es mortal.

---

## 🧩 Cómo funciona

1. **Entrada**: conjunto de cláusulas en CNF.
2. **Refutación**: se añade la negación de la conclusión.
3. **Resolución**: se combinan pares de cláusulas con literales complementarios.
4. **Éxito**: si se deriva la cláusula vacía `□`, el teorema está probado.

---

## 0) Recordatorio teórico (explicado)

1. **Resolución por refutación**

   * Para probar que KB ⊨ α, se añade ¬α a la base y se intenta derivar la cláusula vacía (□).
   * Si llegas a contradicción, α era correcta.
   * Ejemplo: “Sócrates es mortal”.

2. **CNF (Forma Normal Conjuntiva)**

   * Conjunto de cláusulas (cada cláusula es un OR de literales).
   * Toda la base es la conjunción (AND) de esas cláusulas.
   * Resolución solo funciona si la KB está en CNF.

3. **Paso de resolución**

   * Dados dos cláusulas con literales complementarios (p y ¬p), el resolvente es la unión de ambas menos esos literales.
   * Ejemplo: (p ∨ q) y (¬p ∨ r) ⇒ (q ∨ r).

4. **Primer Orden vs. Proposicional**

   * En proposicional, los literales deben coincidir exactamente (p vs. ¬p).
   * En primer orden, puedes unificarlos aplicando sustituciones si predicados y aridades son compatibles.
   * Ejemplo: Padre(x, Ana) y ¬Padre(Juan, y) unifican con {x=Juan, y=Ana}.

5. **Éxito de la prueba**

   * Si aparece la cláusula vacía (□), la refutación fue exitosa.
   * Esto significa que KB ⊨ α: la conclusión se sigue lógicamente de la base.

---

## 🔧 Extensiones posibles

* Parser para transformar expresiones a CNF.
* Estandarización automática de variables.
* Estrategias de optimización: *set-of-support*, *factoring*.

---

✍️ **Autor:** Proyecto académico desarrollado en Python para la clase de Introduccion a IA.
