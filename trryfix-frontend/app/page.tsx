import Header from '@/components/Header'
import Hero from '@/components/Hero'
import Features from '@/components/Features'
import FlowTable from '@/components/FlowTable'

export default function Home() {
  return (
    <main className="min-h-screen">
      <Header />
      <Hero />
      <FlowTable /> 
      <Features />
    </main>
  )
}

