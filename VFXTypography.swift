import Vision
import CoreImage
import AVFoundation

class VFXTypography {
    
    // Tách người ra khỏi nền (Person Segmentation)
    func generateSubjectMask(from frame: CIImage) async -> CIImage? {
        let request = VNGeneratePersonSegmentationRequest()
        request.qualityLevel = .accurate
        request.outputPixelFormat = kCVPixelFormatType_OneComponent8
        
        let handler = VNImageRequestHandler(ciImage: frame, options: [:])
        
        do {
            try handler.perform([request])
            guard let result = request.results?.first as? VNPixelBufferObservation else { return nil }
            
            // CIImage của Mask (Vùng màu trắng là người, đen là nền)
            let maskImage = CIImage(cvPixelBuffer: result.pixelBuffer)
            return maskImage
            
        } catch {
            print("Lỗi phân tích Vision: \(error)")
            return nil
        }
    }
    
    // Logic render (Giả mã cho CoreAnimation)
    // Để áp dụng: 
    // Layer 1: Background Video (AVPlayerLayer)
    // Layer 2: Text Layer (CATextLayer) -> Có hiệu ứng Kinetic
    // Layer 3: Masked Video Layer (Sử dụng maskImage từ hàm trên đè lên)
    func setupDepthAwareLayering(videoLayer: CALayer, textLayer: CATextLayer, maskedSubjectLayer: CALayer) -> CALayer {
        let parentLayer = CALayer()
        
        parentLayer.addSublayer(videoLayer)
        parentLayer.addSublayer(textLayer)
        parentLayer.addSublayer(maskedSubjectLayer)
        
        return parentLayer
    }
}
