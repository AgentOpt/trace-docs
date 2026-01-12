import Link from 'next/link';
import { ArrowRight, Code2, Zap, GitBranch, BookOpen, Github, Sparkles } from 'lucide-react';

export default function HomePage() {
  return (
    <main className="flex flex-1 flex-col">
      {/* Hero Section */}
      <section className="flex flex-col items-center justify-center px-4 py-24 text-center bg-gradient-to-b from-fd-background to-fd-muted/20">
        <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-fd-border bg-fd-muted/50 px-4 py-2 text-sm backdrop-blur">
          <Sparkles className="h-4 w-4 text-fd-primary" />
          <span>AutoDiff for AI Agents</span>
        </div>
        
        <h1 className="mb-6 max-w-4xl text-5xl font-extrabold tracking-tight sm:text-6xl md:text-7xl bg-gradient-to-r from-fd-foreground to-fd-muted-foreground bg-clip-text text-transparent">
          End-to-end Optimization for AI Systems
        </h1>
        
        <p className="mb-10 max-w-2xl text-lg text-fd-muted-foreground sm:text-xl">
          Train AI agents with general feedback like rewards, natural language, or compiler errors.
          Write Python code directly and optimize it like training neural networks.
        </p>

        <div className="flex flex-col gap-4 sm:flex-row">
          <Link
            href="/docs"
            className="group inline-flex items-center gap-2 rounded-lg bg-fd-primary px-6 py-3 text-fd-primary-foreground font-semibold shadow-lg hover:bg-fd-primary/90 transition-all"
          >
            Get Started
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
          </Link>
          
          <Link
            href="https://github.com/AgentOpt/Trace"
            target="_blank"
            className="inline-flex items-center gap-2 rounded-lg border border-fd-border bg-fd-background px-6 py-3 font-semibold hover:bg-fd-muted/50 transition-all"
          >
            <Github className="h-4 w-4" />
            View on GitHub
          </Link>
        </div>

        {/* Quick Stats */}
        <div className="mt-16 grid grid-cols-2 gap-8 sm:grid-cols-4">
          <div className="flex flex-col items-center">
            <div className="text-3xl font-bold text-fd-primary">3</div>
            <div className="text-sm text-fd-muted-foreground">Optimizers</div>
          </div>
          <div className="flex flex-col items-center">
            <div className="text-3xl font-bold text-fd-primary">PyTorch-like</div>
            <div className="text-sm text-fd-muted-foreground">API</div>
          </div>
          <div className="flex flex-col items-center">
            <div className="text-3xl font-bold text-fd-primary">NeurIPS</div>
            <div className="text-sm text-fd-muted-foreground">2024</div>
          </div>
          <div className="flex flex-col items-center">
            <div className="text-3xl font-bold text-fd-primary">Open</div>
            <div className="text-sm text-fd-muted-foreground">Source</div>
          </div>
        </div>
      </section>

      {/* Code Preview Section */}
      <section className="border-t border-fd-border bg-fd-background px-4 py-20">
        <div className="mx-auto max-w-6xl">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Familiar PyTorch-like Syntax</h2>
            <p className="text-fd-muted-foreground text-lg">
              Define trainable parameters and optimize them with a simple, intuitive API
            </p>
          </div>
          
          <div className="rounded-xl border border-fd-border bg-fd-card overflow-hidden shadow-2xl">
            <div className="bg-fd-muted/50 px-4 py-2 border-b border-fd-border flex items-center gap-2">
              <div className="flex gap-1.5">
                <div className="h-3 w-3 rounded-full bg-red-500/80" />
                <div className="h-3 w-3 rounded-full bg-yellow-500/80" />
                <div className="h-3 w-3 rounded-full bg-green-500/80" />
              </div>
              <span className="text-xs text-fd-muted-foreground ml-2">quickstart.py</span>
            </div>
            <pre className="p-6 overflow-x-auto text-sm leading-relaxed">
              <code>{`from opto.trace import node, bundle
from opto.optimizers import OptoPrime

# Define trainable function
@bundle(trainable=True)
def strange_sort_list(lst):
    '''Sort list in strange order: min, max, min, max...'''
    return sorted(lst)

# Optimize with feedback
optimizer = OptoPrime(strange_sort_list.parameters())

for epoch in range(5):
    output = strange_sort_list([1, 2, 3, 4])
    feedback = check_correctness(output)
    
    optimizer.zero_feedback()
    optimizer.backward(output, feedback)
    optimizer.step()  # LLM updates the function!`}</code>
            </pre>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="border-t border-fd-border bg-fd-muted/20 px-4 py-20">
        <div className="mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold mb-4">Why Trace?</h2>
            <p className="text-fd-muted-foreground text-lg">
              A new paradigm for training AI systems end-to-end
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            <div className="rounded-lg border border-fd-border bg-fd-card p-6 shadow-sm hover:shadow-lg transition-shadow">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-fd-primary/10">
                <GitBranch className="h-6 w-6 text-fd-primary" />
              </div>
              <h3 className="mb-2 text-xl font-semibold">Computation Graph</h3>
              <p className="text-fd-muted-foreground">
                Automatically traces execution to build a computation graph, just like autograd but for AI agents.
              </p>
            </div>

            <div className="rounded-lg border border-fd-border bg-fd-card p-6 shadow-sm hover:shadow-lg transition-shadow">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-fd-primary/10">
                <Code2 className="h-6 w-6 text-fd-primary" />
              </div>
              <h3 className="mb-2 text-xl font-semibold">Write Real Code</h3>
              <p className="text-fd-muted-foreground">
                No need to wrap functions in strings. Write actual executable Python code with full IDE support.
              </p>
            </div>

            <div className="rounded-lg border border-fd-border bg-fd-card p-6 shadow-sm hover:shadow-lg transition-shadow">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-fd-primary/10">
                <Zap className="h-6 w-6 text-fd-primary" />
              </div>
              <h3 className="mb-2 text-xl font-semibold">Multiple Optimizers</h3>
              <p className="text-fd-muted-foreground">
                Choose from OptoPrime, OPRO, or TextGrad. Switch optimizers with a single line of code.
              </p>
            </div>

            <div className="rounded-lg border border-fd-border bg-fd-card p-6 shadow-sm hover:shadow-lg transition-shadow">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-fd-primary/10">
                <BookOpen className="h-6 w-6 text-fd-primary" />
              </div>
              <h3 className="mb-2 text-xl font-semibold">Rich Feedback</h3>
              <p className="text-fd-muted-foreground">
                Use any feedback: numerical rewards, natural language, compiler errors, or test results.
              </p>
            </div>

            <div className="rounded-lg border border-fd-border bg-fd-card p-6 shadow-sm hover:shadow-lg transition-shadow">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-fd-primary/10">
                <Sparkles className="h-6 w-6 text-fd-primary" />
              </div>
              <h3 className="mb-2 text-xl font-semibold">LLM Backend Agnostic</h3>
              <p className="text-fd-muted-foreground">
                Works with OpenAI, Anthropic, or any LiteLLM-supported provider. Easy API key management.
              </p>
            </div>

            <div className="rounded-lg border border-fd-border bg-fd-card p-6 shadow-sm hover:shadow-lg transition-shadow">
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-fd-primary/10">
                <Github className="h-6 w-6 text-fd-primary" />
              </div>
              <h3 className="mb-2 text-xl font-semibold">Research-Backed</h3>
              <p className="text-fd-muted-foreground">
                Published at NeurIPS 2024. Battle-tested on NLP, robotics, and multi-agent tasks.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="border-t border-fd-border bg-fd-background px-4 py-20">
        <div className="mx-auto max-w-4xl text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to optimize your AI agents?</h2>
          <p className="text-fd-muted-foreground text-lg mb-8">
            Install Trace and start building self-improving AI systems in minutes.
          </p>
          
          <div className="mb-8 rounded-lg border border-fd-border bg-fd-muted/50 p-4 font-mono text-sm">
            pip install trace-opt
          </div>

          <div className="flex flex-col gap-4 sm:flex-row sm:justify-center">
            <Link
              href="/docs/getting-started"
              className="inline-flex items-center justify-center gap-2 rounded-lg bg-fd-primary px-6 py-3 text-fd-primary-foreground font-semibold hover:bg-fd-primary/90 transition-all"
            >
              Read the Docs
              <ArrowRight className="h-4 w-4" />
            </Link>
            
            <Link
              href="/docs/tutorials"
              className="inline-flex items-center justify-center gap-2 rounded-lg border border-fd-border px-6 py-3 font-semibold hover:bg-fd-muted/50 transition-all"
            >
              View Tutorials
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
