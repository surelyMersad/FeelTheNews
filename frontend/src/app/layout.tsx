import './globals.css'
import { Toaster } from 'react-hot-toast'

export const metadata = {
  title: 'News Sentiment Dashboard',
  description: 'Real-time news sentiment analysis using NYT API and FinBERT',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        {children}
        <Toaster position="top-right" />
      </body>
    </html>
  )
} 