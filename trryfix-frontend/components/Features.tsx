import { Cpu } from 'lucide-react'
import Link from 'next/link'

export default function Features() {
  return (
    <>
      <section className="py-20">
        <h2 className="text-4xl font-bold text-center mb-16">Automated QA sucks...</h2>
        <div className="container mx-auto grid md:grid-cols-3 gap-8 px-4">
          {/* Brittle Tests */}
          <div className="space-y-4">
            <div className="bg-gray-900 rounded-lg p-6 aspect-square flex items-center justify-center">
              <div className="font-mono text-sm opacity-70">
                <pre className="whitespace-pre-wrap">
                  {`<body>
  <div>
    <button class="tsdg121"/>
    <div>
      <a id="cta-email12"/>
    </div>
  </div>
</body>`}
                </pre>
              </div>
            </div>
            <h3 className="text-xl font-semibold">Brittle & flaky tests</h3>
            <p className="text-gray-400">
              Static tests break with every website update, triggering false errors and wasting valuable time.
            </p>
          </div>

          {/* Tedious Setup */}
          <div className="space-y-4">
            <div className="bg-gray-900 rounded-lg p-6 aspect-square flex items-center justify-center">
              <div className="font-mono text-sm">
                <div className="text-gray-400">await page.click(</div>
                <div className="text-red-400">&quot;.widgetth-child(2) .log-1c&quot;</div>
                <div className="text-gray-400">);</div>
                <div className="mt-4 text-red-500">
                  CSS selector &apos;.log-1c&apos;
                  <br />
                  not found in &apos;nth-child(2)&apos;
                </div>
              </div>
            </div>
            <h3 className="text-xl font-semibold">Tedious setup and maintenance</h3>
            <p className="text-gray-400">
              Constantly updating selectors and attributes bogs down your team with tedious upkeep, diverting focus from new features.
            </p>
          </div>

          {/* Blind to UX */}
          <div className="space-y-4">
            <div className="bg-gray-900 rounded-lg p-6 aspect-square flex items-center justify-center">
              <div className="w-full max-w-[200px] space-y-4">
                <div className="flex justify-between items-center">
                  <div className="space-x-1">
                    <span className="inline-block w-2 h-2 rounded-full bg-red-500"/>
                    <span className="inline-block w-2 h-2 rounded-full bg-yellow-500"/>
                    <span className="inline-block w-2 h-2 rounded-full bg-green-500"/>
                  </div>
                </div>
                <div className="space-y-2">
                  <div className="text-lg font-semibold">Sign Up</div>
                  <div className="h-8 bg-gray-800 rounded"/>
                  <div className="h-8 bg-gray-800 rounded"/>
                  <button className="w-full bg-gray-800 rounded h-8"/>
                </div>
              </div>
            </div>
            <h3 className="text-xl font-semibold">Blind to real UX</h3>
            <p className="text-gray-400">
              Code-based tests overlook visual bugs and UX issues, allowing critical problems to slip through until users report them.
            </p>
          </div>
        </div>
      </section>

      <section className="py-20">
        <h2 className="text-4xl font-bold text-center mb-16">Fix AI is a better way to test</h2>
        <div className="flex justify-center mb-16">
          <Cpu className="w-16 h-16" />
        </div>
        <div className="container mx-auto grid md:grid-cols-2 gap-16 px-4">
          <div>
            <h3 className="text-xl font-semibold mb-4">User-like agents</h3>
            <p className="text-gray-400">
              Our agents visually test your website like real users. They navigate your core flows and analyze each screen to catch bugs that your users would otherwise run into.
            </p>
          </div>
          <div>
            <h3 className="text-xl font-semibold mb-4">Fully managed</h3>
            <p className="text-gray-400">
              Fix AI is fully managed. Share your website with us, and we'll build and run high-quality tests for you. <span className="font-bold">Zero</span> setup or maintenance from your end.
            </p>
          </div>
        </div>
        <div className="flex justify-center space-x-6 mt-20">
          <Link href="https://linkedin.com/in/harshkasat" target='_blank' className="opacity-50 hover:opacity-100 transition-opacity">
            <span className="sr-only">LinkedIn</span>
            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
          </Link>
          <Link href="https://x.com/harsh__kasat" target='_blank' className="opacity-50 hover:opacity-100 transition-opacity">
            <span className="sr-only">Twitter</span>
            <svg className="w-6 h-6" viewBox="0 0 24 24" fill="currentColor">
              <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
            </svg>
          </Link>
        </div>
      </section>
    </>
  )
}

