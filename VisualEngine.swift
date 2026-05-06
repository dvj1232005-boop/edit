import AVFoundation
import CoreMedia

class VisualEngine {
    
    func smartBeatSync(rawVideoURLs: [URL], beatTimes: [TimeInterval], audioURL: URL) async throws -> AVMutableComposition {
        let composition = AVMutableComposition()
        
        // 1. Tạo Track Video và Audio
        guard let videoTrack = composition.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid),
              let audioTrack = composition.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid) else {
            throw NSError(domain: "EngineError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Không thể tạo track."])
        }
        
        var currentTime: CMTime = .zero
        var clipIndex = 0
        
        // 2. Cắt ghép video theo Beat
        for i in 0..<(beatTimes.count - 1) {
            let beatDuration = beatTimes[i+1] - beatTimes[i]
            let durationCMTime = CMTime(seconds: beatDuration, preferredTimescale: 600)
            
            let sourceURL = rawVideoURLs[clipIndex % rawVideoURLs.count]
            let sourceAsset = AVURLAsset(url: sourceURL)
            
            guard let sourceVideoTrack = try await sourceAsset.loadTracks(withMediaType: .video).first else { continue }
            
            // Cắt từ đầu clip (Có thể random start time tương tự logic Python)
            let timeRange = CMTimeRange(start: .zero, duration: durationCMTime)
            
            try videoTrack.insertTimeRange(timeRange, of: sourceVideoTrack, at: currentTime)
            
            currentTime = CMTimeAdd(currentTime, durationCMTime)
            clipIndex += 1
        }
        
        // 3. Thêm nhạc nền
        let audioAsset = AVURLAsset(url: audioURL)
        if let sourceAudioTrack = try await audioAsset.loadTracks(withMediaType: .audio).first {
            let audioTimeRange = CMTimeRange(start: .zero, duration: currentTime)
            try audioTrack.insertTimeRange(audioTimeRange, of: sourceAudioTrack, at: .zero)
        }
        
        return composition
    }
}
