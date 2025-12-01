import json
import os
from datetime import datetime
from collections import defaultdict
import re

def load_whales():
    """Load whale data from whales.json."""
    if os.path.exists('whales.json'):
        with open('whales.json', 'r') as f:
            return json.load(f)
    return {}

def load_opportunities():
    """Load opportunities data from opportunities.json."""
    if os.path.exists('opportunities.json'):
        with open('opportunities.json', 'r') as f:
            return json.load(f)
    return {}

def extract_keywords(text):
    """Extract meaningful keywords from text."""
    if not text:
        return set()
    
    # Convert to lowercase and split
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Filter out common words
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'will', 'be', 'is', 'are', 'was', 'were'}
    keywords = {w for w in words if len(w) > 3 and w not in stopwords}
    
    return keywords

def match_market_to_opportunities(market_id, market_question, opportunities):
    """
    Check if a market matches any opportunity sources.
    Returns: (matched_sources_count, matched_sources_list)
    """
    matched_sources = []
    market_keywords = extract_keywords(market_question)
    
    if not market_keywords:
        return 0, []
    
    # Check trending markets
    for trending in opportunities.get('trending', []):
        trending_keywords = extract_keywords(trending.get('question', ''))
        if market_keywords & trending_keywords:  # Intersection
            matched_sources.append(f"Trending: {trending.get('question', '')[:50]}")
            break
    
    # Check keywords
    for keyword in opportunities.get('keywords', []):
        keyword_text = extract_keywords(keyword.get('question', ''))
        if market_keywords & keyword_text:
            matched_sources.append(f"Keyword: {keyword.get('category', '')}")
            break
    
    # Check news
    for news in opportunities.get('news', []):
        news_keywords = extract_keywords(news.get('title', ''))
        if market_keywords & news_keywords:
            matched_sources.append(f"News: {news.get('source', '')}")
            break
    
    # Check reddit
    for reddit in opportunities.get('reddit', []):
        reddit_keywords = extract_keywords(reddit.get('title', ''))
        if market_keywords & reddit_keywords:
            matched_sources.append(f"Reddit: r/{reddit.get('source', '')}")
            break
    
    # Check events
    for event in opportunities.get('events', []):
        event_keywords = extract_keywords(event.get('title', ''))
        if market_keywords & event_keywords:
            matched_sources.append(f"Event: {event.get('title', '')[:50]}")
            break
    
    return len(matched_sources), matched_sources

def analyze_convergence(min_whales=2, min_sources=1):
    """
    Analyze convergence between whale activity and opportunities.
    
    Args:
        min_whales: Minimum number of whales required
        min_sources: Minimum number of information sources required
    
    Returns:
        List of convergent signals
    """
    whales = load_whales()
    opportunities = load_opportunities()
    
    # Group whales by market
    market_whales = defaultdict(list)
    
    for whale_addr, whale_data in whales.items():
        markets = whale_data.get('markets', [])
        for market_id in markets:
            market_whales[market_id].append({
                'address': whale_addr,
                'volume': whale_data.get('total_volume', 0),
                'score': whale_data.get('score', 0)
            })
    
    # Analyze each market
    signals = []
    
    for market_id, whale_list in market_whales.items():
        nb_whales = len(whale_list)
        
        # Skip if not enough whales
        if nb_whales < min_whales:
            continue
        
        # Try to get market question (simplified - in real scenario, fetch from API)
        # For now, use market_id as placeholder
        market_question = f"Market {market_id[:10]}"
        
        # Match with opportunities
        nb_sources, matched_sources = match_market_to_opportunities(
            market_id, 
            market_question, 
            opportunities
        )
        
        # Skip if not enough sources
        if nb_sources < min_sources:
            continue
        
        # Calculate confidence score
        confidence_score = nb_whales + nb_sources
        
        # Create signal
        signal = {
            'market_id': market_id,
            'market_question': market_question,
            'nb_whales': nb_whales,
            'nb_sources': nb_sources,
            'confidence_score': confidence_score,
            'whales': whale_list[:5],  # Top 5 whales
            'sources': matched_sources,
            'detected_at': datetime.now().isoformat()
        }
        
        signals.append(signal)
    
    # Sort by confidence score
    signals.sort(key=lambda x: x['confidence_score'], reverse=True)
    
    return signals

def save_signals(signals):
    """Save convergent signals to JSON file."""
    with open('convergent_signals.json', 'w') as f:
        json.dump(signals, f, indent=2)

if __name__ == "__main__":
    print("🎯 Analyzing Convergent Signals...")
    signals = analyze_convergence(min_whales=2, min_sources=1)
    save_signals(signals)
    print(f"✅ Found {len(signals)} convergent signals")
    for signal in signals[:3]:
        print(f"  - {signal['market_question']}: {signal['nb_whales']} whales + {signal['nb_sources']} sources")
