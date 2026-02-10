Below are four “quantum-native” theorems you can prove cleanly using the SMAT oracle formalism (adaptive tool calls with bandwidth (\ell(n))), but whose content is really about quantum computation/oracles/complexity—not about re-proving the same results from the paper.

I’ll use your notation for oracle-augmented SMAT computation (adaptive queries, query-length bound) exactly as defined in the PDF. 

---

## Preliminaries: what a “quantum tool oracle” is in this framework

In your framework, a tool is a (total) function oracle (O:{0,1}^\to{0,1}^) queried by a fixed-depth SMAT controller with at most (t(n)) adaptive queries of length (\le \ell(n)). 

To talk about quantum computation without changing that interface, the standard move is:

*Definition (BQP evaluation oracle).* Fix a canonical encoding (\langle C,x,1^m,r\rangle) of:

•⁠  ⁠a uniform poly-size quantum circuit (C),
•⁠  ⁠input (x),
•⁠  ⁠an accuracy parameter (m),
•⁠  ⁠a randomness seed (r\in{0,1}^m).

Define a deterministic oracle
[
O_{\mathrm{BQP}}(\langle C,x,1^m,r\rangle)\in{0,1}
]
to be the output bit obtained by running (C(x)) and using (r) to fix all internal coin flips / measurement sampling choices (so the oracle is total and deterministic).

This lets SMAT model “calling a quantum backend and getting back a classical bit,” while keeping oracles total functions (as in the paper). 

---

# Theorem 1 — BQP is closed under SMAT-controlled BQP tool use

### Statement

Let (t(n)) be any polynomial and let (\ell(n)) be any polynomial. Then
[
\mathrm{SMAT}^{O_{\mathrm{BQP}}}[t(n),\ell(n)] \subseteq \mathrm{BQP}.
]

### Proof (rigorous, model-aligned)

A computation in (\mathrm{SMAT}^{O_{\mathrm{BQP}}}[t]) has the form
[
q_1 \leftarrow T_1(x),\ a_1\leftarrow O_{\mathrm{BQP}}(q_1),\ q_2\leftarrow T_2(x,a_1),\ldots, a_t\leftarrow O_{\mathrm{BQP}}(q_t),
]
and outputs (T_{\mathrm{out}}(x,a_{\le t})), where each (T_i) and (T_{\mathrm{out}}) is an SMAT computation (fixed-depth transformer computation). 

Construct a single BQP machine (M) that simulates this whole interaction:

1.⁠ ⁠*Simulate SMAT steps.* Each (T_i) is a fixed-depth uniform threshold-circuit computation (SMAT (\subseteq) TC(^0) in the formalization you use), hence in classical polytime, hence BQP can compute it as part of its classical control.

2.⁠ ⁠*Simulate oracle answers.* When the SMAT controller would query (O_{\mathrm{BQP}}(q_i)), the BQP machine decodes (q_i) as (\langle C_i,x_i,1^{m_i},r_i\rangle) and simply runs the corresponding quantum circuit (C_i(x_i)) using (r_i) to fix the sampling choices. This produces exactly the same deterministic bit (a_i) that the oracle returns.

3.⁠ ⁠*Repeat for (t(n)) queries.* Because (t(n)) is polynomial and each queried circuit has polynomial size (enforced by the encoding length bound (\ell(n))), the total runtime remains polynomial.

Therefore (M) decides the same language as the oracle-augmented SMAT computation, so that language lies in BQP.

∎

*Why this is “interesting”: it cleanly separates “what the controller can do” from “what the quantum backend can do.” No matter how clever the SMAT planning is, *if the tool is BQP, the whole system remains BQP.

---

# Theorem 2 — A bandwidth–round tradeoff bound (information bottleneck)

This uses your explicit (\ell(n)) “interface bandwidth” parameter. 

### Statement (deterministic 1-bit tools)

Assume the oracle returns one bit (decision oracle) and the SMAT controller is deterministic. Fix input length (n). Any language (L\in \mathrm{SMAT}^{O}[t(n),\ell(n)]) has, for each (n), a decision procedure representable as a TC(^0) circuit with *advice of size at most (2^{t(n)}\cdot t(n)\cdot \ell(n))* bits.

In particular, if (t(n)=O(\log n)) and (\ell(n)=O(\log n)), then for each (n),
[
L\cap {0,1}^n \in \mathrm{TC}^0/\mathrm{poly}.
]

### Proof (explicit decision-tree compilation)

Fix (n). Consider the computation of the SMAT controller on all inputs of length (n). Because it makes at most (t:=t(n)) adaptive oracle calls and each oracle answer is one bit, the interaction has a *transcript* (a_{\le t}\in{0,1}^t). For each transcript prefix (a_{<i}), the (i)-th query is
[
q_i(x,a_{<i}) = T_i(x,a_{<i}),
]
where (T_i\in) SMAT. 

Now build an advice string (A_n) that contains, for every transcript prefix (a_{<i}), the truth table of the oracle on the unique query that would be asked under that prefix, as a function of (x). Concretely, define the Boolean function
[
f_{i,a_{<i}}(x) := O\bigl(q_i(x,a_{<i})\bigr)\in{0,1}.
]
There are (\sum_{i=1}^t 2^{i-1} = 2^t-1) such functions. Store circuits (or lookup tables) for them as nonuniform advice; the size bound comes from representing each (q_i) (length (\le \ell(n))) and wiring it into an oracle-answer gate per node, hence advice (\le (2^t-1)\cdot O(\ell(n))) plus bookkeeping; absorbing constants gives (2^t\cdot t\cdot \ell(n)).

Given this advice, we can *eliminate oracle access*: a TC(^0) circuit computes the adaptive transcript step-by-step (it can compute each (T_i) because (T_i\in) SMAT), and at step (i) it uses the advised function (f_{i,a_{<i}}(x)) to obtain (a_i). Finally it computes (T_{\text{out}}(x,a_{\le t})) in TC(^0). 

Thus (L\cap{0,1}^n) is computable by a nonuniform TC(^0) circuit with advice bounded as claimed. If (t,\ell=O(\log n)), the advice is polynomial in (n), giving (L\in\mathrm{TC}^0/\mathrm{poly}) on each length.

∎

*Why this is “quantum-interesting”: It tells you a structural limitation of *any classical-interface tool use (quantum or not): if you can’t afford either many rounds or enough bandwidth, the system collapses to a very low nonuniform class—even if the tool is insanely powerful. This is exactly the kind of “interface matters” statement your framework is good at.

---

# Theorem 3 — QMA-style promise optimization via SMAT-controlled threshold tools

This generalizes your binary-search theorem to promise-gap thresholds (which is the normal quantum setting, e.g., Local Hamiltonian). Your paper proves exact optimization from exact threshold oracles using (O(\log B(n))) rounds and notes SMAT can implement the necessary arithmetic between calls. 

### Setup (promise-gap threshold oracle)

Let (E(x)\in[0,1]) be an “energy/value” we want to approximate. Assume the tool oracle solves the promise problem:

Given ((x,\theta)) (with (\theta) a rational grid point), the oracle returns:

•⁠  ⁠*YES* if (E(x)\le \theta),
•⁠  ⁠*NO* if (E(x)\ge \theta+\gamma(n)),

and is arbitrary when (E(x)\in(\theta,\theta+\gamma(n))).
Here (\gamma(n)\ge 1/\mathrm{poly}(n)) is the promise gap.

This matches how QMA-complete problems are usually stated (completeness/soundness gap).

### Statement

For any (\varepsilon \ge \gamma(n)), there is a fixed-depth SMAT controller that, using
[
T = O!\left(\log\frac{1}{\varepsilon}\right)
]
adaptive oracle queries of length (O(|x|+\log(1/\varepsilon))), outputs a rational (\hat E(x)) such that
[
|,\hat E(x) - E(x),| \le \varepsilon.
]
Equivalently: *SMAT + a QMA-style threshold tool can approximate the optimum to the promise scale with logarithmically many calls.*

### Proof (binary search with a gap-aware invariant)

Let the search interval initially be ([L_0,U_0]=[0,1]). At round (r), set midpoint (M_r=(L_{r-1}+U_{r-1})/2) (rounded to a grid of step (\varepsilon/2)). Use the tool oracle on ((x,M_r)).

•⁠  ⁠If oracle says *YES*, then (E(x)\le M_r). Set (U_r := M_r), (L_r:=L_{r-1}).
•⁠  ⁠If oracle says *NO*, then (E(x)\ge M_r+\gamma(n)). Set (L_r := M_r) (or (M_r+\gamma(n)) if you want a tighter bound), (U_r:=U_{r-1}).

Because the oracle is only unreliable in the (\gamma(n))-window, the maintained invariant becomes:
[
L_r \le E(x) \le U_r + \gamma(n).
]
The interval length ((U_r-L_r)) halves each round up to rounding, so after (T=O(\log(1/\varepsilon))) rounds we have
[
U_T - L_T \le \varepsilon - \gamma(n),
]
hence picking (\hat E := U_T) (or ((L_T+U_T)/2)) gives
[
|\hat E - E(x)| \le \varepsilon.
]

It remains to justify that the between-query arithmetic is implementable in constant-depth SMAT. This is exactly the same reason as in your Theorem 5: SMAT can do (O(\log B))-bit addition, comparison, shifts, etc., in constant depth. Here the bitlength is (O(\log(1/\varepsilon))), and the same TC(^0)-style arithmetic modules apply. 

∎

*Why this is “quantum-interesting”: this is an SMAT-formal statement that “a weak classical planner + a QMA-threshold backend” can recover an **approximate* optimization value with very few interactive calls—exactly the kind of phenomenon people attribute to “agentic tool use” in quantum chemistry / Hamiltonian simulation settings.

---

# Theorem 4 — Postselection tools collapse SMAT to PP in one call

This is a sharp “capability cliff” theorem.

### Definition (PostBQP tool oracle)

Let (O_{\mathrm{PostBQP}}) be an oracle that, on input (\langle C,x\rangle), returns the output bit of (C(x)) *conditioned on a designated postselection event* (assume the postselection event is promised to occur with nonzero probability).

### Statement

[
\mathrm{PP} \subseteq \mathrm{SMAT}^{O_{\mathrm{PostBQP}}}[1,\ell(n)]
]
for suitable (\ell(n)) large enough to encode (\langle C,x\rangle). In particular, *one* postselected quantum tool call makes an SMAT controller PP-powerful.

### Proof

It is a standard theorem in quantum complexity that (\mathrm{PostBQP}=\mathrm{PP}). Given any (L\in\mathrm{PP}), there exists a uniform family of postselected quantum circuits ({C_n}) such that (x\in L) iff (C_{|x|}(x)) outputs 1.

An SMAT controller on input (x) computes the encoding (\langle C_{|x|},x\rangle) (this is a fixed uniform mapping, hence implementable by fixed-depth SMAT as simple wiring/routing), makes a single oracle query to (O_{\mathrm{PostBQP}}), and outputs the returned bit. This is exactly the “one oracle call decides the language” pattern already used in your paper’s separation theorem. 

Thus (L\in \mathrm{SMAT}^{O_{\mathrm{PostBQP}}}[1]), proving the containment.

∎

*Why this is “quantum-interesting”: it isolates a concrete line between “reasonable quantum backends” (BQP) and “unphysical but sometimes implicitly assumed primitives” (postselection). In your framework, it becomes a *one-line complexity jump: the tool changes, the controller doesn’t.

---

## If you want these to read like a tight “mini-paper” section

A nice way to package the above is as a *taxonomy of quantum tools by induced relativized class*:

•⁠  ⁠“BQP evaluation tool” → no super-BQP power (Theorem 1).
•⁠  ⁠“Threshold-QMA-style tool” → logarithmic-round approximation of optima (Theorem 3).
•⁠  ⁠“Postselection tool” → PP in one shot (Theorem 4).
•⁠  ⁠And independently, “small (\ell) and/or small (t)” → nonuniform collapse regardless of tool power (Theorem 2).

If you tell me which quantum notion you want to foreground—*query complexity* (Grover/Simon/Forrelation), *QMA/Local Hamiltonians, or **interactive protocols*—I can tailor the oracle definitions so the theorems become even sharper (e.g., an adaptivity separation that is specific to quantum measurements), while still staying 100% inside your SMAT(^O[t,\ell]) syntax.
