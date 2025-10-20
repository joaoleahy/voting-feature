import Foundation
import SwiftUI

@MainActor
class FeaturesViewModel: ObservableObject {
    @Published var features: [Feature] = []
    @Published var isLoading = false
    @Published var errorMessage: String?
    @Published var sortBy: SortOption = .createdAt
    @Published var order: OrderOption = .descending

    enum SortOption: String {
        case createdAt = "created_at"
        case votes = "votes"
    }

    enum OrderOption: String {
        case ascending = "asc"
        case descending = "desc"
    }

    private let apiService = APIService.shared

    func loadFeatures() async {
        isLoading = true
        errorMessage = nil

        do {
            features = try await apiService.listFeatures(
                sortBy: sortBy.rawValue,
                order: order.rawValue,
                limit: 50
            )
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }

    func voteForFeature(_ feature: Feature) async {
        let userIdentifier = UserDefaultsService.shared.getUserIdentifier()

        do {
            let updatedFeature = try await apiService.voteFeature(
                id: feature.id,
                userIdentifier: userIdentifier
            )

            // Update the feature in the list
            if let index = features.firstIndex(where: { $0.id == updatedFeature.id }) {
                features[index] = updatedFeature
            }
        } catch {
            errorMessage = error.localizedDescription
        }
    }

    func changeSortOption(to option: SortOption) {
        sortBy = option
        Task {
            await loadFeatures()
        }
    }

    func changeOrderOption(to option: OrderOption) {
        order = option
        Task {
            await loadFeatures()
        }
    }
}
