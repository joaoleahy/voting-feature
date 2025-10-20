import Foundation

enum APIError: Error, LocalizedError {
    case invalidURL
    case invalidResponse
    case decodingError
    case serverError(String)

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response from server"
        case .decodingError:
            return "Failed to decode response"
        case .serverError(let message):
            return message
        }
    }
}

class APIService {
    static let shared = APIService()

    private let baseURL: String

    private init() {
        // For iOS Simulator, use localhost
        // For real device, replace with your machine's IP address
        baseURL = "http://localhost:8000"
    }

    // MARK: - Features

    func listFeatures(sortBy: String = "created_at", order: String = "desc", limit: Int = 50) async throws -> [Feature] {
        guard let url = URL(string: "\(baseURL)/api/v1/features?sort_by=\(sortBy)&order=\(order)&limit=\(limit)") else {
            throw APIError.invalidURL
        }

        let (data, response) = try await URLSession.shared.data(from: url)

        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw APIError.invalidResponse
        }

        do {
            let features = try JSONDecoder().decode([Feature].self, from: data)
            return features
        } catch {
            throw APIError.decodingError
        }
    }

    func getFeature(id: String) async throws -> Feature {
        guard let url = URL(string: "\(baseURL)/api/v1/features/\(id)") else {
            throw APIError.invalidURL
        }

        let (data, response) = try await URLSession.shared.data(from: url)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        if httpResponse.statusCode == 404 {
            throw APIError.serverError("Feature not found")
        }

        guard (200...299).contains(httpResponse.statusCode) else {
            throw APIError.invalidResponse
        }

        do {
            let feature = try JSONDecoder().decode(Feature.self, from: data)
            return feature
        } catch {
            throw APIError.decodingError
        }
    }

    func createFeature(title: String, description: String, authorName: String) async throws -> Feature {
        guard let url = URL(string: "\(baseURL)/api/v1/features") else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let createRequest = CreateFeatureRequest(title: title, description: description, authorName: authorName)
        request.httpBody = try JSONEncoder().encode(createRequest)

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        if httpResponse.statusCode == 400 {
            if let errorResponse = try? JSONDecoder().decode([String: String].self, from: data),
               let detail = errorResponse["detail"] {
                throw APIError.serverError(detail)
            }
        }

        guard (200...299).contains(httpResponse.statusCode) else {
            throw APIError.invalidResponse
        }

        do {
            let feature = try JSONDecoder().decode(Feature.self, from: data)
            return feature
        } catch {
            throw APIError.decodingError
        }
    }

    func voteFeature(id: String, userIdentifier: String) async throws -> Feature {
        guard let url = URL(string: "\(baseURL)/api/v1/features/\(id)/vote") else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let voteRequest = VoteRequest(userIdentifier: userIdentifier)
        request.httpBody = try JSONEncoder().encode(voteRequest)

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        if httpResponse.statusCode == 404 {
            throw APIError.serverError("Feature not found")
        }

        if httpResponse.statusCode == 409 {
            throw APIError.serverError("You have already voted for this feature")
        }

        guard (200...299).contains(httpResponse.statusCode) else {
            throw APIError.invalidResponse
        }

        do {
            let feature = try JSONDecoder().decode(Feature.self, from: data)
            return feature
        } catch {
            throw APIError.decodingError
        }
    }
}
