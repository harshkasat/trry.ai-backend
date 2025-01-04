import './globals.css'
import { Inter } from 'next/font/google'

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Fix AI Clone',
  description: 'Find bugs before your users do',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <head><link rel="shortcut icon" href="trryfix-frontend/app/web-coding.png" /></head>
      <body className={`${inter.className} bg-black text-white`}>{children}</body>
    </html>
  )
}

