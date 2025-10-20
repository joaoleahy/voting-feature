import Foundation
import SwiftUI

@MainActor
class CreateFeatureViewModel: ObservableObject {
    @Published var title = ""
    @Published var description = ""
    @Published var authorName = ""
    @Published var isSubmitting = false
    @Published var errorMessage: String?
    @Published var successMessage: String?

    private let apiService = APIService.shared

    var isFormValid: Bool {
        !title.isEmpty && title.count <= 200 &&
        !description.isEmpty &&
        !authorName.isEmpty && authorName.count <= 100
    }

    func createFeature() async -> Bool {
        guard isFormValid else {
            errorMessage = "Please fill in all fields correctly"
            return false
        }

        isSubmitting = true
        errorMessage = nil
        successMessage = nil

        do {
            _ = try await apiService.createFeature(
                title: title,
                description: description,
                authorName: authorName
            )
            successMessage = "Feature created successfully!"
            isSubmitting = false
            return true
        } catch {
            errorMessage = error.localizedDescription
            isSubmitting = false
            return false
        }
    }

    func reset() {
        title = ""
        description = ""
        authorName = ""
        errorMessage = nil
        successMessage = nil
    }
}
