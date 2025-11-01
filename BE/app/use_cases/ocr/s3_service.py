"""Dummy S3 Service for PDF download"""


class S3Service:
    """더미 S3 서비스 - PDF 다운로드를 모킹"""

    def __init__(self):
        pass

    def download_pdf(self, s3_key: str) -> bytes:
        """
        S3에서 PDF 파일을 다운로드 (더미)

        Args:
            s3_key: S3 객체 키 (파일 경로)

        Returns:
            bytes: PDF 파일의 바이트 데이터 (더미)
        """
        # 더미 PDF 바이트 데이터 반환
        return b"%PDF-1.4 dummy content"
