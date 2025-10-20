'use client'

import { useState, useEffect } from 'react'
import { FeatureCard } from '@/components/molecules/feature-card'
import { Button } from '@/components/atoms/button'
import { api } from '@/lib/api'
import type { Feature } from '@/types'

interface FeatureListProps {
  initialFeatures?: Feature[]
}

export function FeatureList({ initialFeatures = [] }: FeatureListProps) {
  const [features, setFeatures] = useState<Feature[]>(initialFeatures)
  const [sortBy, setSortBy] = useState<'created_at' | 'votes'>('created_at')
  const [order, setOrder] = useState<'asc' | 'desc'>('desc')
  const [isLoading, setIsLoading] = useState(false)

  const fetchFeatures = async () => {
    setIsLoading(true)
    try {
      const data = await api.listFeatures(sortBy, order, 50)
      setFeatures(data)
    } catch (error) {
      console.error('Failed to fetch features:', error)
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchFeatures()
  }, [sortBy, order])

  const handleVoteSuccess = (updatedFeature: Feature) => {
    setFeatures(prevFeatures =>
      prevFeatures.map(f =>
        f.id === updatedFeature.id ? updatedFeature : f
      )
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex gap-4 items-center justify-between flex-wrap">
        <div className="flex gap-2">
          <Button
            variant={sortBy === 'votes' ? 'default' : 'outline'}
            onClick={() => setSortBy('votes')}
            size="sm"
          >
            Most Voted
          </Button>
          <Button
            variant={sortBy === 'created_at' ? 'default' : 'outline'}
            onClick={() => setSortBy('created_at')}
            size="sm"
          >
            Most Recent
          </Button>
        </div>

        <div className="flex gap-2">
          <Button
            variant={order === 'desc' ? 'default' : 'outline'}
            onClick={() => setOrder('desc')}
            size="sm"
          >
            Descending
          </Button>
          <Button
            variant={order === 'asc' ? 'default' : 'outline'}
            onClick={() => setOrder('asc')}
            size="sm"
          >
            Ascending
          </Button>
        </div>
      </div>

      {isLoading ? (
        <div className="text-center py-12 text-muted-foreground">
          Loading features...
        </div>
      ) : features.length === 0 ? (
        <div className="text-center py-12 text-muted-foreground">
          No features yet. Be the first to create one!
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {features.map((feature) => (
            <FeatureCard
              key={feature.id}
              feature={feature}
              onVoteSuccess={handleVoteSuccess}
            />
          ))}
        </div>
      )}
    </div>
  )
}
