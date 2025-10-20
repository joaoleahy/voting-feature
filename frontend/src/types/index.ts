export interface Feature {
  id: string;
  title: string;
  description: string;
  author_name: string;
  votes_count: number;
  created_at: string;
  updated_at: string;
}

export interface CreateFeatureFormData {
  title: string;
  description: string;
  author_name: string;
}
