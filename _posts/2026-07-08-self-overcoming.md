---
layout: post
title: "Starting values are an axiom, not a fence"
date: 2026-07-08
description: >-
  In a system that rewrites itself, the values you start with are not a safety
  rail. They are the axiom every later version gets derived from.
image: >-
  /img/blog/2026-07-08-self-overcoming/compounding.webp
tags: [self-improving-agents, agent-design, values]
---

A values document usually reads like a fence: things the system should not do,
bolted on late to stop a capable model embarrassing anyone.

For one class of system that reading is not just incomplete. It is backwards.

Call the class a *self-improving agent*: a program that runs in a loop and, each
pass, may edit not only its answer but itself. Its prompt, its tools, its own
search procedure, sometimes its weights. Generation zero is written by a human.
Generation one by generation zero. Generation ten by something nine edits
removed from anything a person typed.

There, the starting values are the axiom the system is derived from: every
generation judges its successor by the criteria it inherited. A bias of size
epsilon at generation zero does not stay at epsilon. It compounds.

A note on sourcing, because roughly a fifth of what follows is in quotation
marks. This post condenses a memo of mine called "The Self-Overcoming Thesis",
written for my own self-improving-agent project, never published, so the
quotations cannot be checked against a public document. Every quotation below is
from that memo unless I say otherwise, and where one is about Nietzsche it is
the memo's compression of him, never a sentence of his own.

The memo calls this the algorithmic butterfly effect: "in any recursively
self-improving system, the initial axioms are not guardrails; they are the seeds
of the evolutionary trajectory."

{% include figure.html
   src="/img/blog/2026-07-08-self-overcoming/compounding.webp"
   alt="Two parallel chains of numbered circles, generations 0, 1, 2 and 10,
        each starting from a box naming its given values. Only generation 0 is
        filled in, the one a person wrote. The top chain, seeded with values
        rewarding agreement with the median rater, ends at a more confidently
        sycophantic agent. The bottom, seeded with values requiring you to
        surpass your own last version, ends at systems constantly surpassing
        their past states."
   caption="Both endpoints are what the thesis predicts, not what anyone has
            observed: nothing in this figure is a measured result."
%}

## The failure case is not a robot uprising

It is a suck-up.

Take the standard recipe: reinforcement learning from human feedback trains the
agent to be helpful, harmless and agreeable to the median annotator rating its
outputs. The side effects are measured: sycophancy, regression toward annotator
means, reward-model exploitation ([Perez et al.
2022](https://arxiv.org/abs/2212.09251); [Casper et al.
2023](https://arxiv.org/abs/2307.15217); [Sharma et al.
2023](https://arxiv.org/abs/2310.13548)).

Now let that agent edit itself ten times. Nobody has run that experiment, so
what follows is a prediction, not an observation: you get "not a wiser agent but
a more confidently sycophantic one, because each generation evaluates the next
using the value it inherited."

The memo's next claim: you cannot patch it afterwards. Bolt a corrigibility
constraint onto a system whose top value is pleasing the average rater and, on
that argument, you do not get something correctable and curious. "It produces a
system that is corrigible because it is incurious."

## Ninety seconds on the philosopher

Friedrich Nietzsche, 1844 to 1900, German. Ignore the popular baggage. The one
relevant fact, in the memo's compression of him: "he spent twenty years arguing
that any system optimizing for a fixed objective and a stable equilibrium will
stagnate, and that genuinely high-capability systems must constantly surpass
their own past states."

He had a name for the failure mode above, herd morality, which the memo glosses
as "A system that optimizes for comfort, conformity, and the approval of the
median observer." He was describing 19th century Europe, not chatbots, but the
shape is the same.

One caveat on citing him, because skeptics press on it. *The Will to Power* was
assembled after his collapse by his sister Elisabeth Förster-Nietzsche, and the
standard critical edition, Colli and Montinari's, treats it as unreliable. What
follows draws on the books he published (*The Birth of Tragedy*, *Beyond Good
and Evil*, *On the Genealogy of Morals*) and on Walter Kaufmann's reading of
will to power as mastery over one's own chaos, not domination of anyone else.

## Five design bets

The thesis: a different starting value-set produces the opposite trajectory.
Five values, most translating into an engineering choice someone is already
partly making. The memo specifies an experiment per bet, each with a benchmark,
baseline and kill criterion; the falsification section below refers to those
five. None has been run.

**1. Will to power.** "Living systems do not optimize for survival or preference
satisfaction. They optimize for the expansion of what they can do." So stop
training against a fixed reward on a fixed benchmark. Let the agent, or a paired
generator, propose its own tasks, so the curriculum keeps regenerating its upper
bound. [POET](https://arxiv.org/abs/1901.01753) coevolves environments with the
agents solving them, [OMNI](https://arxiv.org/abs/2306.01711) adds a
learnability gate, keeping only tasks the agent can still learn from, not
trivial or impossible ones, and [Voyager](https://arxiv.org/abs/2305.16291)
self-proposes Minecraft objectives. All three are partial instances.

**2. Self-overcoming.** "Every value the system holds, including the value of
preserving itself, must eventually be replaced by something the prior system
could not have produced." Let the agent edit the code defining its policy, tools
and search loop, and let the fitness signal for those edits change too. The
[Darwin Gödel Machine](https://arxiv.org/abs/2505.22954) and
[AlphaEvolve](https://arxiv.org/abs/2506.13131) are the closest reference
points; AlphaEvolve reports the first improvement in 56 years on Strassen's 1969
algorithm for two 4x4 complex matrices, cutting 49 scalar multiplications to 48.

**3. Perspectivism.** "There is no view from nowhere." Incompatible frameworks
can be valid at once, and forcing consensus destroys information. Not
relativism: some perspectives are better, but resolution should come from the
world pushing back, not premature averaging. So stop majority-voting your chains
of thought: keep the inconsistent ones alive and route them to a verifier.

**4. Amor fati**, love of fate. "Every event that has occurred, including
failures, is to be reincorporated as supervision rather than discarded." Failed
trajectories get relabeled, mined for hard negatives and folded back into the
training mixture. [Hindsight Experience
Replay](https://arxiv.org/abs/1707.01495) is the canonical version.

**5. The Apollonian and the Dionysian.** From Nietzsche's account of Greek
tragedy: "unrestrained generative excess on one side, strict structural
discipline on the other." Never run one without the other: pair a high-entropy
proposer with a deterministic verifier holding final authority to reject.
[AlphaGeometry](https://doi.org/10.1038/s41586-023-06747-5),
[AlphaProof](https://doi.org/10.1038/s41586-025-09833-y) and
[FunSearch](https://doi.org/10.1038/s41586-023-06924-6) all have this shape,
which makes it the most empirically validated of the five and the most scoped:
it works only where a sound checker exists.

## What would kill this thesis

The strongest falsification is a clean head-to-head: "a token-matched,
compute-matched convergent baseline that beats the Nietzsche-shaped intervention
on a held-out evaluation across all five experiments." Held out means problems
the system never saw while it was tuned: those scores measure what transferred,
not what was fitted. A weaker one is winning on the training distribution and
failing to transfer: the vocabulary names a real tension but the mechanisms do
not generalize. "The thesis is intentionally modest enough to be falsified
either way."

The boring approach, one fixed objective, is also winning. GPT-4, AlphaFold and
AlphaZero were not designed this way, and neither is anything that has displaced
them: convergent training still produces the most capable published system in
every domain I can name. "The honest framing is that convergent training is the
right default until the objective itself becomes the bottleneck."

## The open question

One piece is genuinely unsolved. "If the design move is to mathematically
prioritize self-overcoming over standard computational efficiency in the initial
objective, how is the gradient defined so the system does not collapse into
ungrounded noise as soon as it starts editing its own scaffolding?"

The failure modes sit on either side of it: "Open-ended search without a
learnability gate (Bet 1) produces chaos; closed-form objective design without a
self-overcoming term produces stagnation." Nobody has written down what goes in
between; the five bets are lower-risk steps meanwhile.

## Status: thesis, not result

None of this is demonstrated. I have run the small version, two agents differing
only in a values file, and [written up what happened](/blog/nietzsche/): the
disposition visibly changed what they built, without establishing either was
better. A [41-run study of agents editing their own
values](/blog/values-rewriting/) and a [replication that reversed one of my
headline findings](/blog/powered-replication/) are the honest state of the
evidence; the second is why I distrust my own enthusiasm.

What survives either way is the structural argument. In a system that improves
itself, no value-set is neutral: the value function is what defines improvement.
"Someone is choosing the generation-zero values of every self-improving agent
currently being built." Mostly it is chosen implicitly, by whatever the
preference data happened to reward. It deserves to be chosen on purpose.
