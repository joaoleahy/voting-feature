'use client'

import Link from 'next/link'
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/atoms/card'
import { Badge } from '@/components/atoms/badge'
import { VoteButton } from './vote-button'
import type { Feature } from '@/types'

interface FeatureCardProps {
  feature: Feature
  onVoteSuccess?: (updatedFeature: Feature) => void
}

export function FeatureCard({ feature, onVoteSuccess }: FeatureCardProps) {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    })
  }

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader>
        <div className="flex justify-between items-start">
          <Link href={`/features/${feature.id}`} className="flex-1">
            <CardTitle className="text-xl hover:text-primary transition-colors cursor-pointer">
              {feature.title}
            </CardTitle>
          </Link>
          <VoteButton feature={feature} onVoteSuccess={onVoteSuccess} />
        </div>
      </CardHeader>
      <CardContent>
        <p className="text-muted-foreground line-clamp-2">{feature.description}</p>
      </CardContent>
      <CardFooter className="flex justify-between items-center text-sm text-muted-foreground">
        <span>by {feature.author_name}</span>
        <span>{formatDate(feature.created_at)}</span>
      </CardFooter>
    </Card>
  )
}
