import Foundation

class UserDefaultsService {
    static let shared = UserDefaultsService()

    private let userIdKey = "user_identifier"

    private init() {}

    func getUserIdentifier() -> String {
        if let existingId = UserDefaults.standard.string(forKey: userIdKey) {
            return existingId
        }

        let newId = "user_\(UUID().uuidString)"
        UserDefaults.standard.set(newId, forKey: userIdKey)
        return newId
    }
}
