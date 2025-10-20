import { FeatureList } from '@/components/organisms/feature-list'

export default function Home() {
  return (
    <div className="space-y-8">
      <div className="text-center space-y-2">
        <h1 className="text-4xl font-bold">Feature Requests</h1>
        <p className="text-muted-foreground text-lg">
          Vote for the features you want to see next
        </p>
      </div>

      <FeatureList />
    </div>
  )
}
