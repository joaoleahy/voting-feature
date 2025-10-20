'use client'

import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/atoms/card'
import { Button } from '@/components/atoms/button'
import { Badge } from '@/components/atoms/badge'
import { VoteButton } from '@/components/molecules/vote-button'
import { api } from '@/lib/api'
import { ArrowLeft } from 'lucide-react'
import type { Feature } from '@/types'

export default function FeatureDetailPage() {
  const params = useParams()
  const router = useRouter()
  const [feature, setFeature] = useState<Feature | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchFeature = async () => {
      try {
        const data = await api.getFeature(params.id as string)
        setFeature(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load feature')
      } finally {
        setIsLoading(false)
      }
    }

    fetchFeature()
  }, [params.id])

  if (isLoading) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">Loading feature...</p>
      </div>
    )
  }

  if (error || !feature) {
    return (
      <div className="max-w-2xl mx-auto">
        <Card>
          <CardHeader>
            <CardTitle>Error</CardTitle>
            <CardDescription>{error || 'Feature not found'}</CardDescription>
          </CardHeader>
          <CardFooter>
            <Button onClick={() => router.push('/')} variant="outline">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back to Home
            </Button>
          </CardFooter>
        </Card>
      </div>
    )
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const handleVoteSuccess = (updatedFeature: Feature) => {
    setFeature(updatedFeature)
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <Button onClick={() => router.push('/')} variant="outline" size="sm">
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Features
      </Button>

      <Card>
        <CardHeader>
          <div className="flex justify-between items-start gap-4">
            <div className="flex-1">
              <CardTitle className="text-3xl mb-2">{feature.title}</CardTitle>
              <CardDescription className="text-base">
                Submitted by {feature.author_name} on {formatDate(feature.created_at)}
              </CardDescription>
            </div>
            <VoteButton feature={feature} onVoteSuccess={handleVoteSuccess} />
          </div>
        </CardHeader>
        <CardContent>
          <div className="prose max-w-none">
            <p className="text-lg whitespace-pre-wrap">{feature.description}</p>
          </div>
        </CardContent>
        <CardFooter className="flex justify-between items-center border-t pt-6">
          <div className="text-sm text-muted-foreground">
            Last updated: {formatDate(feature.updated_at)}
          </div>
          <Badge variant="secondary" className="text-base px-4 py-2">
            {feature.votes_count} {feature.votes_count === 1 ? 'vote' : 'votes'}
          </Badge>
        </CardFooter>
      </Card>
    </div>
  )
}
