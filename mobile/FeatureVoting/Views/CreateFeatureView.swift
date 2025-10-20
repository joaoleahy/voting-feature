import SwiftUI

struct CreateFeatureView: View {
    @StateObject private var viewModel = CreateFeatureViewModel()
    @Binding var isPresented: Bool
    let onSuccess: () -> Void

    var body: some View {
        NavigationView {
            Form {
                Section(header: Text("Feature Details")) {
                    TextField("Title", text: $viewModel.title)
                        .textInputAutocapitalization(.sentences)

                    VStack(alignment: .leading, spacing: 4) {
                        TextEditor(text: $viewModel.description)
                            .frame(minHeight: 100)

                        Text("\(viewModel.description.count) characters")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }

                Section(header: Text("Author Information")) {
                    TextField("Your Name", text: $viewModel.authorName)
                        .textInputAutocapitalization(.words)
                }

                Section {
                    Button(action: {
                        Task {
                            let success = await viewModel.createFeature()
                            if success {
                                isPresented = false
                                onSuccess()
                            }
                        }
                    }) {
                        HStack {
                            Spacer()
                            if viewModel.isSubmitting {
                                ProgressView()
                                    .progressViewStyle(CircularProgressViewStyle())
                                    .padding(.trailing, 8)
                                Text("Creating...")
                            } else {
                                Text("Create Feature")
                                    .fontWeight(.semibold)
                            }
                            Spacer()
                        }
                    }
                    .disabled(!viewModel.isFormValid || viewModel.isSubmitting)
                }
            }
            .navigationTitle("New Feature")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        isPresented = false
                    }
                    .disabled(viewModel.isSubmitting)
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
        }
    }
}

struct CreateFeatureView_Previews: PreviewProvider {
    static var previews: some View {
        CreateFeatureView(isPresented: .constant(true), onSuccess: {})
    }
}
