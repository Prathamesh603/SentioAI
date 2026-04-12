"""
Performance metrics tracking and analysis
Tracks response times, quality metrics, and sentiment analysis
"""

from datetime import datetime, timedelta
from typing import Dict, List
from core.logger import get_logger

logger = get_logger("applog")


class MetricsTracker:
    """Track and analyze chatbot performance metrics"""
    
    def __init__(self):
        """Initialize metrics tracker"""
        self.responses = []
        self.created_at = datetime.now()
        logger.info("MetricsTracker initialized")
    
    def add_response(self, user_input: str, bot_response: str, metadata: dict) -> None:
        """
        Record a new response with metrics
        
        Args:
            user_input: User's input text
            bot_response: Bot's response text
            metadata: Response metadata (sentiment, timing, etc.)
        """
        try:
            response_record = {
                "user_input": user_input,
                "bot_response": bot_response,
                "metadata": metadata,
                "timestamp": datetime.now(),
                "input_length": len(user_input),
                "output_length": len(bot_response)
            }
            self.responses.append(response_record)
            
            response_time = metadata.get("response_time", 0)
            logger.info(f"Response recorded (input: {len(user_input)} chars, output: {len(bot_response)} chars, time: {response_time:.2f}s)")
        
        except Exception as e:
            logger.error(f"Error adding response to metrics: {str(e)}")
    
    def get_metrics_summary(self) -> Dict:
        """
        Get comprehensive metrics summary
        
        Returns:
            Dictionary with aggregated metrics
        """
        try:
            if not self.responses:
                logger.debug("No responses recorded yet, returning empty metrics")
                return {
                    "total_exchanges": 0,
                    "avg_response_time": 0.0,
                    "avg_response_length": 0,
                    "total_input_chars": 0,
                    "overall_rating": 0.0
                }
            
            response_times = [r["metadata"].get("response_time", 0) for r in self.responses]
            response_lengths = [r["output_length"] for r in self.responses]
            input_lengths = [r["input_length"] for r in self.responses]
            sentiments = [r["metadata"].get("sentiment", "neutral") for r in self.responses]
            
            avg_response_time = sum(response_times) / len(response_times) if response_times else 0
            avg_response_length = sum(response_lengths) / len(response_lengths) if response_lengths else 0
            
            # Calculate sentiment distribution
            positive_count = sentiments.count("positive")
            negative_count = sentiments.count("negative")
            neutral_count = sentiments.count("neutral")
            
            # Calculate overall rating (0-5 scale)
            speed_rating = self._calculate_speed_rating(avg_response_time)
            engagement_rating = self._calculate_engagement_rating(avg_response_length)
            quality_rating = self._calculate_quality_rating(sentiments)
            
            overall_rating = (speed_rating + engagement_rating + quality_rating) / 3
            
            summary = {
                "total_exchanges": len(self.responses),
                "avg_response_time": avg_response_time,
                "avg_response_length": avg_response_length,
                "total_input_chars": sum(input_lengths),
                "total_output_chars": sum(response_lengths),
                "positive_sentiment": positive_count,
                "negative_sentiment": negative_count,
                "neutral_sentiment": neutral_count,
                "avg_confidence": self._avg_confidence(),
                "overall_rating": overall_rating
            }
            
            logger.debug(f"Metrics summary generated: {overall_rating:.2f} overall rating")
            return summary
        
        except Exception as e:
            logger.error(f"Error calculating metrics summary: {str(e)}")
            return {}
    
    def get_overall_rating(self) -> float:
        """
        Get overall quality rating (0-5 scale)
        
        Returns:
            Overall rating value
        """
        try:
            rating = self.get_metrics_summary().get("overall_rating", 0.0)
            logger.debug(f"Overall rating: {rating:.2f}")
            return rating
        except Exception as e:
            logger.error(f"Error getting overall rating: {str(e)}")
            return 0.0
    
    def _calculate_speed_rating(self, avg_time: float) -> float:
        """
        Calculate speed rating based on response time
        
        Args:
            avg_time: Average response time in seconds
        
        Returns:
            Speed rating (0-5)
        """
        if avg_time < 0.5:
            return 5.0
        elif avg_time < 1.0:
            return 4.8
        elif avg_time < 2.0:
            return 4.5
        elif avg_time < 5.0:
            return 4.0
        elif avg_time < 10.0:
            return 3.0
        else:
            return 2.0
    
    def _calculate_engagement_rating(self, avg_length: float) -> float:
        """
        Calculate engagement rating based on response length
        
        Args:
            avg_length: Average response length in characters
        
        Returns:
            Engagement rating (0-5)
        """
        # Ideal response: 200-500 characters
        if 200 <= avg_length <= 500:
            return 5.0
        elif 100 <= avg_length < 200 or 500 < avg_length <= 1000:
            return 4.0
        elif 50 <= avg_length < 100 or 1000 < avg_length <= 1500:
            return 3.0
        else:
            return 2.0
    
    def _calculate_quality_rating(self, sentiments: List[str]) -> float:
        """
        Calculate quality rating based on sentiment
        
        Args:
            sentiments: List of sentiment labels
        
        Returns:
            Quality rating (0-5)
        """
        if not sentiments:
            return 3.0
        
        positive = sentiments.count("positive")
        negative = sentiments.count("negative")
        total = len(sentiments)
        
        # Higher positive ratio = higher quality
        positive_ratio = positive / total
        negative_ratio = negative / total
        
        base_score = 3.0  # Neutral baseline
        base_score += positive_ratio * 2.0  # +2 points for full positive
        base_score -= negative_ratio * 1.5  # -1.5 points for full negative
        
        return min(5.0, max(1.0, base_score))
    
    def _avg_confidence(self) -> float:
        """
        Calculate average confidence score across all responses
        
        Returns:
            Average confidence (0-1)
        """
        try:
            if not self.responses:
                return 0.0
            
            confidences = [r["metadata"].get("confidence", 0) for r in self.responses]
            return sum(confidences) / len(confidences) if confidences else 0.0
        
        except Exception as e:
            logger.error(f"Error calculating average confidence: {str(e)}")
            return 0.0
    
    def get_detailed_analytics(self) -> Dict:
        """
        Get detailed analytics for dashboard visualization
        
        Returns:
            Dictionary with detailed analytics
        """
        try:
            if not self.responses:
                logger.debug("No responses for detailed analytics")
                return {}
            
            analytics = {
                "session_duration": str(datetime.now() - self.created_at),
                "total_conversations": len(self.responses),
                "conversation_flow": self._analyze_conversation_flow(),
                "topical_summary": self._get_topical_summary(),
                "performance_trend": self._get_performance_trend()
            }
            
            logger.debug("Detailed analytics generated")
            return analytics
        
        except Exception as e:
            logger.error(f"Error generating detailed analytics: {str(e)}")
            return {}
    
    def _analyze_conversation_flow(self) -> str:
        """Analyze conversation flow pattern"""
        try:
            if len(self.responses) < 2:
                return "Conversation just started"
            
            input_lengths = [r["input_length"] for r in self.responses]
            
            if input_lengths[-1] > input_lengths[0] * 1.5:
                return "Expanding (questions getting longer)"
            elif input_lengths[-1] < input_lengths[0] * 0.7:
                return "Narrowing (questions getting shorter)"
            else:
                return "Stable (consistent conversation flow)"
        
        except Exception as e:
            logger.error(f"Error analyzing conversation flow: {str(e)}")
            return "Unable to analyze"
    
    def _get_topical_summary(self) -> str:
        """Get summary of conversation topics"""
        try:
            if not self.responses:
                return "No conversations yet"
            
            total_chars = sum(r["input_length"] for r in self.responses)
            return f"Total input: {total_chars} characters across {len(self.responses)} messages"
        
        except Exception as e:
            logger.error(f"Error getting topical summary: {str(e)}")
            return "Unable to summarize"
    
    def _get_performance_trend(self) -> str:
        """Get performance trend over time"""
        try:
            if len(self.responses) < 2:
                return "Not enough data for trend analysis"
            
            recent_responses = self.responses[-5:]
            first_half = self.responses[:len(self.responses)//2]
            second_half = self.responses[len(self.responses)//2:]
            
            first_avg_time = sum(r["metadata"].get("response_time", 0) for r in first_half) / len(first_half)
            second_avg_time = sum(r["metadata"].get("response_time", 0) for r in second_half) / len(second_half)
            
            if second_avg_time < first_avg_time:
                return "Performance improving (getting faster)"
            elif second_avg_time > first_avg_time:
                return "Performance declining (getting slower)"
            else:
                return "Performance stable (consistent speed)"
        
        except Exception as e:
            logger.error(f"Error analyzing performance trend: {str(e)}")
            return "Unable to analyze"
