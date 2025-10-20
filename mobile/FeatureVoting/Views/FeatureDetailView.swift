import SwiftUI

struct FeatureDetailView: View {
    @StateObject private var viewModel: FeatureDetailViewModel
    @Environment(\.dismiss) private var dismiss

    init(featureId: String) {
        _viewModel = StateObject(wrappedValue: FeatureDetailViewModel(featureId: featureId))
    }

    var body: some View {
        ScrollView {
            if viewModel.isLoading {
                ProgressView("Loading feature...")
                    .padding()
            } else if let feature = viewModel.feature {
                VStack(alignment: .leading, spacing: 20) {
                    // Header with vote button
                    HStack(alignment: .top) {
                        VStack(alignment: .leading, spacing: 8) {
                            Text(feature.title)
                                .font(.title)
                                .fontWeight(.bold)

                            HStack {
                                Text("by \(feature.authorName)")
                                    .font(.subheadline)
                                    .foregroundColor(.secondary)

                                Spacer()

                                Text(feature.formattedDate)
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }

                        Spacer()

                        Button(action: {
                            Task {
                                await viewModel.voteForFeature()
                            }
                        }) {
                            VStack(spacing: 4) {
                                Image(systemName: "arrow.up")
                                    .font(.title2)
                                Text("\(feature.votesCount)")
                                    .font(.headline)
                            }
                            .padding(.horizontal, 16)
                            .padding(.vertical, 12)
                            .background(Color.blue)
                            .foregroundColor(.white)
                            .cornerRadius(12)
                        }
                    }

                    Divider()

                    // Description
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Description")
                            .font(.headline)

                        Text(feature.description)
                            .font(.body)
                            .foregroundColor(.primary)
                    }

                    Divider()

                    // Stats
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text("Total Votes")
                                .font(.caption)
                                .foregroundColor(.secondary)
                            Text("\(feature.votesCount)")
                                .font(.title2)
                                .fontWeight(.bold)
                        }

                        Spacer()

                        VStack(alignment: .trailing, spacing: 4) {
                            Text("Last Updated")
                                .font(.caption)
                                .foregroundColor(.secondary)
                            Text(formatDateTime(feature.updatedAt))
                                .font(.subheadline)
                        }
                    }
                    .padding()
                    .background(Color(UIColor.secondarySystemBackground))
                    .cornerRadius(12)
                }
                .padding()
            } else {
                VStack(spacing: 16) {
                    Image(systemName: "exclamationmark.triangle")
                        .font(.system(size: 60))
                        .foregroundColor(.orange)
                    Text("Feature not found")
                        .font(.headline)
                }
                .padding()
            }
        }
        .navigationBarTitleDisplayMode(.inline)
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
            await viewModel.loadFeature()
        }
    }

    private func formatDateTime(_ dateString: String) -> String {
        let formatter = ISO8601DateFormatter()
        formatter.formatOptions = [.withInternetDateTime, .withFractionalSeconds]

        guard let date = formatter.date(from: dateString) else {
            return dateString
        }

        let displayFormatter = DateFormatter()
        displayFormatter.dateStyle = .medium
        displayFormatter.timeStyle = .short

        return displayFormatter.string(from: date)
    }
}
