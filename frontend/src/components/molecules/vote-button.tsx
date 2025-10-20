'use client'

import { useState } from 'react'
import { ArrowBigUp } from 'lucide-react'
import { Button } from '@/components/atoms/button'
import { api } from '@/lib/api'
import { useToast } from '@/hooks/use-toast'
import type { Feature } from '@/types'

interface VoteButtonProps {
  feature: Feature
  onVoteSuccess?: (updatedFeature: Feature) => void
}

export function VoteButton({ feature, onVoteSuccess }: VoteButtonProps) {
  const [isVoting, setIsVoting] = useState(false)
  const [voteCount, setVoteCount] = useState(feature.votes_count)
  const { toast } = useToast()

  const handleVote = async (e: React.MouseEvent) => {
    e.preventDefault()
    e.stopPropagation()

    if (isVoting) return

    const userIdentifier = localStorage.getItem('user_id') || `user_${Date.now()}`
    if (!localStorage.getItem('user_id')) {
      localStorage.setItem('user_id', userIdentifier)
    }

    setIsVoting(true)

    const optimisticCount = voteCount + 1
    setVoteCount(optimisticCount)

    try {
      const updatedFeature = await api.voteFeature(feature.id, { user_identifier: userIdentifier })
      setVoteCount(updatedFeature.votes_count)

      if (onVoteSuccess) {
        onVoteSuccess(updatedFeature)
      }

      toast({
        title: "Success!",
        description: "Your vote has been recorded.",
      })
    } catch (error) {
      setVoteCount(voteCount)
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : "Failed to vote",
        variant: "destructive",
      })
    } finally {
      setIsVoting(false)
    }
  }

  return (
    <Button
      onClick={handleVote}
      disabled={isVoting}
      variant="outline"
      size="sm"
      className="flex items-center gap-1 min-w-[70px]"
    >
      <ArrowBigUp className="h-4 w-4" />
      <span className="font-semibold">{voteCount}</span>
    </Button>
  )
}
