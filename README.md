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

## 📑 Sustentación recomendada

* Explicar la diferencia entre **proposicional** y **primer orden**.
* Mostrar el flujo: *CNF → añadir negación de conclusión → resolución → cláusula vacía*.
* Resaltar el papel de la **unificación** en la segunda etapa.
* Señalar limitaciones: las fórmulas deben estar en CNF de antemano.

---

## 🔧 Extensiones posibles

* Parser para transformar expresiones a CNF.
* Estandarización automática de variables.
* Estrategias de optimización: *set-of-support*, *factoring*.

---

✍️ **Autor:** Proyecto académico desarrollado en Python para la clase de Lógica y Algoritmos de Inferencia.
