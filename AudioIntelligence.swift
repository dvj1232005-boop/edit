import Foundation
import Speech
import AVFoundation

class AudioIntelligence {
    private let speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: "vi-VN")) // Hoặc en-US
    
    func extractLyrics(from audioURL: URL, completion: @escaping ([(text: String, start: TimeInterval, end: TimeInterval)]) -> Void) {
        let request = SFSpeechURLRecognitionRequest(url: audioURL)
        request.shouldReportPartialResults = false
        
        speechRecognizer?.recognitionTask(with: request, resultHandler: { result, error in
            guard let result = result, error == nil else {
                print("Lỗi nhận diện âm thanh: \(String(describing: error))")
                completion([])
                return
            }
            
            var wordsData: [(String, TimeInterval, TimeInterval)] = []
            
            // Trích xuất từng từ và timestamp
            for segment in result.bestTranscription.segments {
                wordsData.append((
                    text: segment.substring,
                    start: segment.timestamp,
                    end: segment.timestamp + segment.duration
                ))
            }
            
            if result.isFinal {
                completion(wordsData)
            }
        })
    }
}
