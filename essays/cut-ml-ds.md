# Four defences against fooling yourself — and the times my own verifier was the bug

*The general cut. No finance required; the domain is only the worked example.*

---

I spent most of a project trying to falsify my own result. The result held up. Three separate claims
about *how well I had verified it* did not — each caught by a check I had written specifically to catch
that class of error, and each of which I believed until it failed.

The pattern is worth naming, because it was not random. Every one of the failures was the same failure:
**the claim was broader than the mechanism underneath it.** *"Reproduces bit-for-bit."* *"The certificate
is correct."* *"The comparison reads the file exactly."* Each of those is a property of the artefact plus
its dependency graph, plus the machine, plus my own reading of what the check proved — and none of that
was written down anywhere until a check disagreed with me.

Here are the four defences I built, and what each one actually bought.

## Defence 1 — freeze before looking

Write the decision rule where you cannot reach it after seeing the number, and date it. Metric,
threshold, comparison, the exact rule that converts results into a verdict.

It is usually described as an ethical practice. It is better understood as a mechanism, because its value
is exactly the set of things it makes impossible: moving the bar, swapping the reference point,
quietly dropping the model that embarrassed you. And it has a specific payoff for a single pre-registered
comparison. The usual answer to "you tried several things" is a multiple-testing correction — but if you
fire exactly once, the correction is inert. What binds instead is the **choice of baseline**, because
that is the one input to the test you select. Post hoc, there is always a flattering one.

Freezing is necessary and it is not sufficient. It stops you changing the rule after looking. It does
*not* stop you looking — and I lost my own confirmatory test precisely there.

## Defence 2 — prove the absence of leakage mechanically

"We reviewed the pipeline and it doesn't leak" is a claim about code, and reading code is not a proof. So
leakage is a test suite: each test is an executable definition of one specific way a time-series pipeline
can see the future. Not a checklist, not a review — a suite that fails when the property is violated.

The reason this matters is that **a test can be defeated by something that is not a leak at all.** My
estimator layer produced covariance estimates differing in the last bit for two logically identical input
frames, because pandas reduces along a block's memory strides and a single row assignment is enough to
leave a frame in Fortran order. My suite includes a bit-identical determinism requirement, and under that
requirement my own memory layout was **indistinguishable from leaked information**: the test would have
reported my numerical noise as a leak, and I would have spent a week looking for a leak that was never
there. The fix is one explicit contiguity guarantee; the durable artefact is the test that pins it.

And a test can pass for the wrong reason, which you have to say out loud. One test in my suite is
**vacuous** — the condition it tests for cannot occur in my sample. It is recorded as a skip with the
reason, not as a pass. A green check with no power behind it is worse than a red one, because it buys
silence.

## Defence 3 — certify the numerics

Every one of my 1,176 optimiser solves is checked against a KKT residual, with no fallback solver. Final
state: zero rejections, worst residual 1.49e-11 against a 1e-7 acceptance bar.

That sentence is nearly worthless on its own, because it describes the endpoint. What makes it worth
something is that **the certificate was wrong three times**:

- It recovered a Lagrange multiplier by a method whose fallback path is empty in exactly the case it was
  meant to handle, and that fallback **rejected seven provably optimal solutions** (residuals up to
  1.5e-3) while three independent solvers agreed on the objective to 1e-10.
- A *redundant* constraint — a non-negativity bound already implied by the variable's own defining
  constraints — added a row to the solver's constraint matrix and changed its path, moving one solution to
  a point 2.8e-11 below the optimum. Mathematically equivalent; numerically not.
- Worst of all: **the script doing the certifying was solving a different problem.** It rebuilt the loop by
  hand and passed one method a different starting state than production did. It reported that method clean
  while production was rejecting solves. Evidence the artefact did not produce is not evidence.

A verifier is software. It has bugs, and its bugs are more dangerous than the ones it is looking for,
because they are wrong in the direction of "everything is fine".

## The verification layer's own bugs, and the claim that survived being falsified twice

My two nastiest bugs were both in the comparison scripts, and both produced plausible numbers.

The first snapshot verifier rejected **every valid** input, because the manifest's file list and its
content hash covered different sets of files — four versus five. The first comparison of an archived
dataset against a published table reported an `8.3e-17` mismatch, because **`pandas.read_csv` is lossy by
one unit in the last place at its defaults**: it returns `0.1820065203183531` where the file contains
`0.18200652031835318`. Only `float_precision="round_trip"` is exact. A default setting, behaving as
documented, silently failing a 17-digit equality test.

Then the real one. I had written that my pipeline reproduces its published table **bit-for-bit**, and
added a CI step that could test it. The check failed on its first run, by `4.2e-17`, on one of eighteen
columns. Nothing was wrong with my logic: that metric reached a BLAS kernel that OpenBLAS selects *at run
time* from the CPU's feature set, so the summation order had never been specified by me at all. I
replaced it with a summation whose every rounding step is defined by IEEE-754 — bit-identical anywhere,
and slightly more accurate. Then I measured the cost of the fix instead of asserting it: regenerate,
diff all 46 columns. Exactly one moved, in its last three bits; no headline number moved.

The next run failed **harder**: thirteen of eighteen columns, the worst by `4.698e-12`.

I ruled out the boring explanations rather than assuming them. Identical install sets — 51 packages,
parsed as sets, symmetric difference empty — on an identical runner image. Not dependency drift. Thread
count? I ran the whole pipeline at one BLAS thread and at four: byte-identical output, both matching the
published table. Not threading. The diagnosis fell out of one column that is a function of the fitted
parameters alone, so the two machines had fit slightly *different models*, and the metric differences were
downstream. The magnitude named the layer: a rounding difference here is `1e-16`, and the largest
difference was `4.698e-12` — four orders of magnitude bigger — a `1e-16` input difference amplified by an
optimiser whose own acceptance tolerance is `1e-14`.

That is not fixable, and pretending otherwise would have been the mistake. **A number produced by a solver
is a property of the data, the code and the machine — not just the first two.** So I stopped making one
claim and started making two:

- **Decisions are exact.** Which methods ran, how many refits, how many folds, the headline cost level,
  the ranking, which baseline was selected. Discrete, they are what the experiment is *for*, and a
  `1e-12` wobble cannot move them. Any difference fails the build.
- **Measurements are bounded.** The continuous metrics are compared within a documented `1e-9` — about
  200 times the worst measured cross-platform difference — and the observed worst difference is printed
  on every run, so the bound is spent in public rather than asserted.

The check now runs on every push and prints the difference it actually saw (`4.698e-12`), not the bound it
was allowed. That claim is the only one in the project that has been falsified twice and then survived:
the third machine to run it differed on the measurements by exactly the amount the bound had been set to
absorb, and agreed on everything that decides.

## Defence 4 — significance, materiality and robustness together

Each of the first three defences can be satisfied while the conclusion is still wrong, because overfitting
is not the only way to fool yourself — you also fool yourself by optimising the decision rule. So the rule
is a conjunction: a result must be statistically significant, materially large, *and* stable across
subsamples. Any one alone is a Goodhart target; you can hit it by choosing the wrong thing to measure.

The live demonstration: my two candidate models passed a p-value test against one reference and failed a
significance test against another. Two honest statistics, answering two different questions, disagreeing —
and the rule requires both. A single number would have hidden the entire finding.

## What a reader can take

1. **Freeze the rule before looking**, and date it.
2. **Prove the absence of leakage mechanically.** "We reviewed it" is not a defence — and record the tests
   that are vacuous instead of letting them pass.
3. **Certify the numerics**, and remember the certificate is software too.
4. **Require significance, materiality and robustness together.**

And when you write down what your pipeline guarantees, state it at the strength your check actually has:
exactly where it is exact, bounded where it is bounded, with the measured number printed rather than the
tolerance quoted. That is the whole lesson, and it took three falsifications of my own claims to learn it.
