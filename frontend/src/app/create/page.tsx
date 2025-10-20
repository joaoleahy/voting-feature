import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/atoms/card'
import { FeatureForm } from '@/components/molecules/feature-form'

export default function CreateFeaturePage() {
  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <CardHeader>
          <CardTitle className="text-3xl">Create Feature Request</CardTitle>
          <CardDescription>
            Submit your feature idea and let others vote on it
          </CardDescription>
        </CardHeader>
        <CardContent>
          <FeatureForm />
        </CardContent>
      </Card>
    </div>
  )
}
