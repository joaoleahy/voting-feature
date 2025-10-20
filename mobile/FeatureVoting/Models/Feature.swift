import Foundation

struct Feature: Codable, Identifiable {
    let id: String
    let title: String
    let description: String
    let authorName: String
    var votesCount: Int
    let createdAt: String
    let updatedAt: String

    enum CodingKeys: String, CodingKey {
        case id
        case title
        case description
        case authorName = "author_name"
        case votesCount = "votes_count"
        case createdAt = "created_at"
        case updatedAt = "updated_at"
    }

    var formattedDate: String {
        let formatter = ISO8601DateFormatter()
        formatter.formatOptions = [.withInternetDateTime, .withFractionalSeconds]

        guard let date = formatter.date(from: createdAt) else {
            return createdAt
        }

        let displayFormatter = DateFormatter()
        displayFormatter.dateStyle = .medium
        displayFormatter.timeStyle = .none

        return displayFormatter.string(from: date)
    }
}

struct CreateFeatureRequest: Codable {
    let title: String
    let description: String
    let authorName: String

    enum CodingKeys: String, CodingKey {
        case title
        case description
        case authorName = "author_name"
    }
}

struct VoteRequest: Codable {
    let userIdentifier: String

    enum CodingKeys: String, CodingKey {
        case userIdentifier = "user_identifier"
    }
}
