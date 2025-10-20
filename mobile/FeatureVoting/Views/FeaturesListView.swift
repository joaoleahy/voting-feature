import SwiftUI

struct FeaturesListView: View {
    @StateObject private var viewModel = FeaturesViewModel()
    @State private var showingCreateFeature = false

    var body: some View {
        NavigationView {
            ZStack {
                if viewModel.isLoading && viewModel.features.isEmpty {
                    ProgressView("Loading features...")
                } else if viewModel.features.isEmpty {
                    VStack(spacing: 16) {
                        Image(systemName: "tray")
                            .font(.system(size: 60))
                            .foregroundColor(.gray)
                        Text("No features yet")
                            .font(.headline)
                            .foregroundColor(.secondary)
                        Text("Be the first to create one!")
                            .font(.subheadline)
                            .foregroundColor(.secondary)
                    }
                } else {
                    ScrollView {
                        LazyVStack(spacing: 12) {
                            ForEach(viewModel.features) { feature in
                                NavigationLink(destination: FeatureDetailView(featureId: feature.id)) {
                                    FeatureCardView(feature: feature) {
                                        Task {
                                            await viewModel.voteForFeature(feature)
                                        }
                                    }
                                }
                                .buttonStyle(PlainButtonStyle())
                            }
                        }
                        .padding()
                    }
                    .refreshable {
                        await viewModel.loadFeatures()
                    }
                }
            }
            .navigationTitle("Feature Voting")
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Menu {
                        Section("Sort By") {
                            Button(action: {
                                viewModel.changeSortOption(to: .createdAt)
                            }) {
                                Label("Most Recent", systemImage: viewModel.sortBy == .createdAt ? "checkmark" : "")
                            }

                            Button(action: {
                                viewModel.changeSortOption(to: .votes)
                            }) {
                                Label("Most Voted", systemImage: viewModel.sortBy == .votes ? "checkmark" : "")
                            }
                        }

                        Section("Order") {
                            Button(action: {
                                viewModel.changeOrderOption(to: .descending)
                            }) {
                                Label("Descending", systemImage: viewModel.order == .descending ? "checkmark" : "")
                            }

                            Button(action: {
                                viewModel.changeOrderOption(to: .ascending)
                            }) {
                                Label("Ascending", systemImage: viewModel.order == .ascending ? "checkmark" : "")
                            }
                        }
                    } label: {
                        Image(systemName: "line.3.horizontal.decrease.circle")
                    }
                }

                ToolbarItem(placement: .navigationBarTrailing) {
                    Button(action: {
                        showingCreateFeature = true
                    }) {
                        Image(systemName: "plus")
                    }
                }
            }
            .sheet(isPresented: $showingCreateFeature) {
                CreateFeatureView(isPresented: $showingCreateFeature) {
                    Task {
                        await viewModel.loadFeatures()
                    }
                }
            }
            .alert("Error", isPresented: .constant(viewModel.errorMessage != nil)) {
                Button("OK") {
                    viewModel.errorMessage = nil
                }
            } message: {
                if let errorMessage = viewModel.errorMessage {
                    Text(errorMessage)
                }
            }
            .task {
                await viewModel.loadFeatures()
            }
        }
    }
}

struct FeaturesListView_Previews: PreviewProvider {
    static var previews: some View {
        FeaturesListView()
    }
}
