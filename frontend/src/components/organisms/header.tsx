'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { Button } from '@/components/atoms/button'
import { Plus, Home } from 'lucide-react'

export function Header() {
  const pathname = usePathname()

  return (
    <header className="border-b bg-background sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2">
            <h1 className="text-2xl font-bold text-primary">Feature Voting</h1>
          </Link>

          <nav className="flex items-center gap-4">
            {pathname !== '/' && (
              <Link href="/">
                <Button variant="outline" size="sm">
                  <Home className="h-4 w-4 mr-2" />
                  Home
                </Button>
              </Link>
            )}

            {pathname !== '/create' && (
              <Link href="/create">
                <Button size="sm">
                  <Plus className="h-4 w-4 mr-2" />
                  New Feature
                </Button>
              </Link>
            )}
          </nav>
        </div>
      </div>
    </header>
  )
}
