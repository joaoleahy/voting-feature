import Foundation
import SwiftUI

@MainActor
class FeatureDetailViewModel: ObservableObject {
    @Published var feature: Feature?
    @Published var isLoading = false
    @Published var errorMessage: String?

    private let apiService = APIService.shared
    let featureId: String

    init(featureId: String) {
        self.featureId = featureId
    }

    func loadFeature() async {
        isLoading = true
        errorMessage = nil

        do {
            feature = try await apiService.getFeature(id: featureId)
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }

    func voteForFeature() async {
        guard let currentFeature = feature else { return }

        let userIdentifier = UserDefaultsService.shared.getUserIdentifier()

        do {
            feature = try await apiService.voteFeature(
                id: currentFeature.id,
                userIdentifier: userIdentifier
            )
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}
