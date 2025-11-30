from datetime import datetime
import math

class WhaleAnalyzer:
    def __init__(self):
        pass

    def analyze_whale(self, address, stats):
        """
        Analyze a single whale's statistics and return a score and detailed metrics.
        
        Args:
            address (str): Wallet address
            stats (dict): Dictionary containing 'total_volume', 'trade_count', 'markets', 'first_seen', 'last_trade'
            
        Returns:
            dict: Enhanced stats with 'score', 'activity_level', 'tags'
        """
        volume = stats.get('total_volume', 0)
        trade_count = stats.get('trade_count', 0)
        market_count = len(stats.get('markets', []))
        
        # Calculate Score (0-100)
        # Weights: Volume (50%), Activity (30%), Diversity (20%)
        
        # Volume Score (Logarithmic scale, max score at $1M)
        volume_score = min(100, math.log(max(1, volume), 10) * 16.6) # log10(1M) = 6, 6 * 16.6 ~= 100
        
        # Activity Score (Based on trade count, max at 100 trades)
        activity_score = min(100, trade_count)
        
        # Diversity Score (Based on unique markets, max at 20 markets)
        diversity_score = min(100, market_count * 5)
        
        total_score = (volume_score * 0.5) + (activity_score * 0.3) + (diversity_score * 0.2)
        
        # Determine Tags
        tags = []
        if volume > 100000:
            tags.append("Mega Whale")
        elif volume > 10000:
            tags.append("Whale")
        else:
            tags.append("Dolphin")
            
        if trade_count > 50:
            tags.append("High Frequency")
            
        if market_count > 10:
            tags.append("Diversified")
        elif market_count == 1:
            tags.append("Sniper")

        return {
            **stats,
            "score": round(total_score, 2),
            "metrics": {
                "volume_score": round(volume_score, 2),
                "activity_score": round(activity_score, 2),
                "diversity_score": round(diversity_score, 2)
            },
            "tags": tags
        }

    def rank_whales(self, whales_data):
        """
        Rank whales by score.
        """
        analyzed_whales = {}
        for address, stats in whales_data.items():
            analyzed_whales[address] = self.analyze_whale(address, stats)
            
        # Sort by score descending
        sorted_whales = dict(sorted(analyzed_whales.items(), key=lambda x: x[1]['score'], reverse=True))
        return sorted_whales
