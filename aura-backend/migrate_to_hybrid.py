"""
Database migration script for hybrid model
Adds new columns: age, gender, call_failures
Renames: tenure -> tenure_months
"""
import sqlite3
from pathlib import Path

def migrate_database():
    """Migrate database to hybrid model schema"""
    db_path = Path("aura_dev.db")
    
    if not db_path.exists():
        print("❌ Database not found. Run seed_database.py first.")
        return
    
    print("=" * 60)
    print("Migrating database to hybrid model schema")
    print("=" * 60)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if migration is needed
        cursor.execute("PRAGMA table_info(customers)")
        columns = {row[1] for row in cursor.fetchall()}
        
        if 'age' in columns and 'call_failures' in columns:
            print("✅ Database already migrated!")
            return
        
        print("\n📝 Adding new columns...")
        
        # Add new columns with default values
        if 'age' not in columns:
            cursor.execute("ALTER TABLE customers ADD COLUMN age INTEGER DEFAULT 35")
            print("   ✓ Added 'age' column")
        
        if 'gender' not in columns:
            cursor.execute("ALTER TABLE customers ADD COLUMN gender INTEGER DEFAULT 0")
            print("   ✓ Added 'gender' column")
        
        if 'call_failures' not in columns:
            cursor.execute("ALTER TABLE customers ADD COLUMN call_failures INTEGER DEFAULT 0")
            print("   ✓ Added 'call_failures' column")
        
        # Rename tenure to tenure_months (SQLite doesn't support RENAME COLUMN directly)
        if 'tenure' in columns and 'tenure_months' not in columns:
            # Create new column
            cursor.execute("ALTER TABLE customers ADD COLUMN tenure_months INTEGER")
            # Copy data
            cursor.execute("UPDATE customers SET tenure_months = tenure")
            print("   ✓ Copied 'tenure' to 'tenure_months'")
            print("   ⚠️  Note: Old 'tenure' column still exists (SQLite limitation)")
        
        conn.commit()
        
        print("\n📊 Updating with realistic values...")
        
        # Update with realistic random values
        cursor.execute("""
            UPDATE customers 
            SET 
                age = 18 + ABS(RANDOM() % 62),
                gender = ABS(RANDOM() % 2),
                call_failures = CASE 
                    WHEN complaint_count > 2 THEN ABS(RANDOM() % 15) + 5
                    WHEN complaint_count > 0 THEN ABS(RANDOM() % 10) + 2
                    ELSE ABS(RANDOM() % 5)
                END
        """)
        
        conn.commit()
        
        print("   ✓ Updated age, gender, call_failures with realistic values")
        
        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("=" * 60)
        
        # Show summary
        cursor.execute("SELECT COUNT(*) FROM customers")
        count = cursor.fetchone()[0]
        print(f"\n📈 Updated {count} customer records")
        
        # Show sample
        cursor.execute("""
            SELECT customer_id, name, tenure_months, age, gender, call_failures, 
                   complaint_count, monthly_charge 
            FROM customers 
            LIMIT 3
        """)
        
        print("\n📋 Sample records:")
        print("-" * 60)
        for row in cursor.fetchall():
            print(f"  {row[0]}: {row[1]}")
            print(f"    Tenure: {row[2]} months, Age: {row[3]}, Gender: {row[4]}")
            print(f"    Call Failures: {row[5]}, Complaints: {row[6]}, Charge: ₺{row[7]}")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
