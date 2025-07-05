from collections import defaultdict
from itertools import combinations
from decimal import Decimal
from .models import Order, OrderItem, Product


class ProductRecommendation:
    def __init__(self):
        self.min_support = 0.008
        self.min_confidence = 0.1
        self.rules_cache = {}
        self.association_rules = None
        
    @staticmethod
    # Lấy dữ liệu từ lịch sử đơn hàng
    def get_transaction_data():
        transactions = defaultdict(set)
        orders = Order.objects.all()
        
        for order in orders:
            order_items = OrderItem.objects.filter(order=order)
            transactions[order.id] = set(item.product.id for item in order_items)
            
        return transactions
    
     # Tính tần suất xuất hiện của các set item bằng thuật toán Apriori
    def calculate_frequent_itemsets(self, transactions):
        items = set()
        for transaction in transactions.values():
            items.update(transaction)
            
        # Tính tần suất của từng item riêng lẻ
        item_counts = defaultdict(int)
        for transaction in transactions.values():
            for item in transaction:
                item_counts[frozenset([item])] += 1
                
        min_support_count = self.min_support * len(transactions)
        
        # Loại bỏ các item có tần suất nhỏ hơn min suppport
        frequent_items = {item: count for item, count in item_counts.items() 
                        if count >= min_support_count}
        
        # Xét các cặp item (k = 2) và tăng dần lên thành bộ 3, bộ 4 item (k = 3, 4)
        k = 2
        frequent_itemsets = [frequent_items]
        
        while True:
            candidates = set()
            prev_frequent = set(frequent_itemsets[-1].keys())
            for item1 in prev_frequent:
                for item2 in prev_frequent:
                    union = item1.union(item2)
                    if len(union) == k and union not in candidates:
                        candidates.add(union)
            
            itemset_counts = defaultdict(int)
            for transaction in transactions.values():
                for candidate in candidates:
                    if candidate.issubset(transaction):
                        itemset_counts[candidate] += 1
            
            frequent_k = {itemset: count for itemset, count in itemset_counts.items()
                        if count >= min_support_count}
            
            if not frequent_k:
                break
                
            frequent_itemsets.append(frequent_k)
            k += 1
            
        return frequent_itemsets
    
    # Tạo ra các luật kết hợp từ các itemset phổ biến
    def generate_rules(self, frequent_itemsets):
        rules = []
        
        for k in range(1, len(frequent_itemsets)):
            for itemset, support in frequent_itemsets[k].items():
                for i in range(1, len(itemset)):
                    for antecedent in combinations(itemset, i):
                        antecedent = frozenset(antecedent)
                        consequent = itemset - antecedent
                        
                        antecedent_support = frequent_itemsets[len(antecedent)-1][antecedent]
                        confidence = support / antecedent_support
                        
                        if confidence >= self.min_confidence:
                            rules.append({
                                'antecedent': antecedent,
                                'consequent': consequent,
                                'support': support,
                                'confidence': confidence
                            })
        
        return rules
    
    def update_rules(self):
        # Cập nhật luật kết hợp từ dữ liệu mới
        transactions = self.get_transaction_data()
        if not transactions:
            return
            
        frequent_itemsets = self.calculate_frequent_itemsets(transactions)
        self.association_rules = self.generate_rules(frequent_itemsets)
        
        self.rules_cache = defaultdict(list)
        for rule in self.association_rules:
            for product_id in rule['antecedent']:
                self.rules_cache[product_id].append(rule)
    
    @classmethod
    # Lấy ra 6 sản phẩm được đề xuất dựa trên sản phẩm hiện tại
    def get_recommendations_for_product(cls, product, max_recommendations=6):
        instance = cls()
        
        # Cập nhật luật kết hợp nếu chưa có
        if not instance.association_rules:
            instance.update_rules()
            
        if not instance.rules_cache:
            return cls.get_fallback_recommendations(product, max_recommendations)
        
        exclude_ids = {product.id}
            
        # Lấy ra các luật kết hợp cho sản phẩm hiện tại
        product_rules = instance.rules_cache.get(product.id, [])
        
        # Sắp xếp luật kết hợp dựa trên confidence
        product_rules.sort(key=lambda x: x['confidence'], reverse=True)
        
        # Lấy ra các sản phẩm được đề xuất từ luật kết hợp
        recommended_ids = set()
        for rule in product_rules:
            recommended_ids.update(rule['consequent'])
            if len(recommended_ids) >= max_recommendations:
                break
                
        exclude_ids.update(recommended_ids)
            
        # Lấy ra các sản phẩm được đề xuất
        recommended_products = list(Product.objects.filter(id__in=recommended_ids))
        
        # Nếu vẫn chưa đủ, thêm các sản phẩm dựa trên giá
        # if len(recommended_products) < max_recommendations:
        #     fallback_count = max_recommendations - len(recommended_products)
        #     fallback_products = cls.get_fallback_recommendations(
        #         product, 
        #         fallback_count,
        #         exclude_ids=exclude_ids
        #     )
        #     recommended_products.extend(fallback_products)
            
        return recommended_products[:max_recommendations]
    
    # @staticmethod
    # Lấy ra các sản phẩm dựa trên giá nếu không có luật kết hợp
    # def get_fallback_recommendations(product, count, exclude_ids=None):
    #     exclude_ids = exclude_ids or set()
    #     exclude_ids.add(product.id)
        
    #     min_price = product.price * Decimal('0.7')
    #     max_price = product.price * Decimal('1.3')
        
    #     similar_products = Product.objects.filter(
    #         status=product.status,
    #         price__range=(min_price, max_price)
    #     ).exclude(
    #         id__in=exclude_ids
    #     )
        
    #     if similar_products.count() < count:
    #         # Lấy ra các sản phẩm trong khoảng giá tương tự
    #         price_range_products = Product.objects.filter(
    #             price__range=(min_price, max_price)
    #         ).exclude(
    #             id__in=exclude_ids
    #         )
    #         similar_products = similar_products.union(price_range_products)
            
    #     return similar_products.order_by('-rating')[:count]
    
    def train_model(self):
        print("\nStarting Model Training")
        print(f"Parameters: min_support={self.min_support}, min_confidence={self.min_confidence}")
        
        # Lấy dữ liệu
        transactions = self.get_transaction_data()
        print(f"\nFound {len(transactions)} transactions in total")
        
        if not transactions:
            print("No transaction data available. Training aborted.")
            return
        
        self.update_rules()
        
        # Tính tần suất xuất hiện của các itemset
        frequent_itemsets = self.calculate_frequent_itemsets(transactions)
        print(f"\nFrequent Itemsets Statistics:")
        for k, itemsets in enumerate(frequent_itemsets, 1):
            if itemsets:
                print(f"- {k}-itemsets: {len(itemsets)} found")
        
        # Tạo ra các luật kkết hợp
        rules = self.generate_rules(frequent_itemsets)
        
        if rules:
            print(f"\nTraining Results:")
            print(f"Generated {len(rules)} association rules")
            
            # Sắp xếp theo độ tin cậy
            sorted_rules = sorted(rules, key=lambda x: x['confidence'], reverse=True)
            
            print("\nTop 10 Association Rules:")
            print("----------------------------------")
            for i, rule in enumerate(sorted_rules[:10], 1):
                antecedent_products = Product.objects.filter(id__in=rule['antecedent'])
                consequent_products = Product.objects.filter(id__in=rule['consequent'])
                
                print(f"\n{i}. Rule:")
                print(f"   IF purchases: {', '.join(p.name for p in antecedent_products)}")
                print(f"   THEN likely to buy: {', '.join(p.name for p in consequent_products)}")
                print(f"   Confidence: {rule['confidence']:.2%}")
                print(f"   Support: {rule['support']} transactions")
                
            avg_confidence = sum(r['confidence'] for r in rules) / len(rules)
            avg_support = sum(r['support'] for r in rules) / len(rules)
            print(f"\nOverall Statistics:")
            print(f"Average Confidence: {avg_confidence:.2%}")
            print(f"Average Support: {avg_support:.1f} transactions")
            
        else:
            print("\nNo association rules were generated. This might indicate:")
            print("Insufficient transaction data")
            print("Min support/confidence thresholds too high")
            print(f"Current settings: min_support={self.min_support}, min_confidence={self.min_confidence}")
        
        print("\nTraining Completed")
        


