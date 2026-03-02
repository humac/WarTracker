#!/usr/bin/env python3
"""
Data Collection Script

Collects conflict events from configured data sources and stores them in the database.

Usage:
    python scripts/collect_data.py
    
    Options:
        --sources gdelt,acled,newsapi  # Specify sources (default: all enabled)
        --limit 100                     # Max records per source
        --dry-run                       # Collect but don't save to DB
"""
import asyncio
import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.collectors.manager import CollectorManager
from app.database import get_db
from app.models import ConflictEvent, Source
from sqlalchemy.orm import Session


async def collect_and_store(dry_run: bool = False, sources: list = None, limit: int = None):
    """
    Collect data from sources and store in database.
    
    Args:
        dry_run: If True, collect but don't save
        sources: List of source names to collect from
        limit: Max records per source
    """
    print(f"🌍 WarTracker Data Collection")
    print(f"Started: {datetime.utcnow().isoformat()}")
    print(f"Dry run: {dry_run}")
    print(f"Sources: {sources or 'all enabled'}")
    print("-" * 50)
    
    # Initialize collector manager
    manager = CollectorManager()
    
    if limit:
        # Update max_records for GDELT collector
        if "gdelt" in manager.collectors:
            manager.collectors["gdelt"].max_records = limit
    
    # Collect events
    events = await manager.collect_all(sources=sources)
    
    if not events:
        print("\n⚠️  No events collected")
        return
    
    print(f"\n📊 Collection Summary:")
    print(f"  Total events: {len(events)}")
    for source, count in manager.stats["by_source"].items():
        print(f"  - {source}: {count} events")
    
    if dry_run:
        print("\n💡 Dry run - not saving to database")
        print("\nSample events:")
        for i, event in enumerate(events[:3], 1):
            print(f"\n  {i}. {event['title']}")
            print(f"     Type: {event['event_type']}, Severity: {event['severity_score']}")
            print(f"     Location: {event['latitude']}, {event['longitude']}")
            print(f"     Date: {event['event_timestamp']}")
        return
    
    # Save to database
    print(f"\n💾 Saving to database...")
    
    db = next(get_db())
    try:
        saved_count = 0
        
        for event_data in events:
            try:
                # Create ConflictEvent from dict
                event = ConflictEvent(**event_data)
                db.add(event)
                saved_count += 1
            except Exception as e:
                print(f"  ⚠️  Error saving event: {e}")
                continue
        
        db.commit()
        print(f"✅ Saved {saved_count} events to database")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Database error: {e}")
        raise
    finally:
        db.close()
    
    # Print summary
    print(f"\n✅ Collection complete!")
    print(f"   Total collected: {manager.stats['total_collected']}")
    print(f"   Total saved: {saved_count}")
    if manager.stats["errors"]:
        print(f"   Errors: {len(manager.stats['errors'])}")
        for error in manager.stats["errors"]:
            print(f"     - {error['source']}: {error['error']}")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Collect conflict event data")
    parser.add_argument(
        "--sources", 
        type=str, 
        default=None,
        help="Comma-separated list of sources (default: all enabled)"
    )
    parser.add_argument(
        "--limit", 
        type=int, 
        default=100,
        help="Max records per source (default: 100)"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Collect but don't save to database"
    )
    
    args = parser.parse_args()
    
    # Parse sources
    sources = None
    if args.sources:
        sources = [s.strip() for s in args.sources.split(",")]
    
    # Run collection
    asyncio.run(collect_and_store(
        dry_run=args.dry_run,
        sources=sources,
        limit=args.limit
    ))


if __name__ == "__main__":
    main()
