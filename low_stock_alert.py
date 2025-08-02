@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def low_stock_alerts(company_id):
    alerts = []
    
    # Fetch warehouses for the company
    warehouses = Warehouse.query.filter_by(company_id=company_id).all()
    
    for wh in warehouses:
        inventory_items = db.session.query(
            Product, ProductInventory, Supplier
        ).join(ProductInventory, Product.id == ProductInventory.product_id
        ).outerjoin(SupplierProducts, Product.id == SupplierProducts.product_id
        ).outerjoin(Supplier, Supplier.id == SupplierProducts.supplier_id
        ).filter(ProductInventory.warehouse_id == wh.id).all()

        for product, inventory, supplier in inventory_items:
            # Assume a threshold table or default threshold
            threshold = get_threshold_for_product(product.id)  # stub function
            recent_sale = check_recent_sales(product.id)  # stub function

            if not recent_sale:
                continue

            if inventory.quantity < threshold:
                days_left = estimate_days_until_stockout(product.id, inventory.quantity)
                alerts.append({
                    "product_id": product.id,
                    "product_name": product.name,
                    "sku": product.sku,
                    "warehouse_id": wh.id,
                    "warehouse_name": wh.name,
                    "current_stock": inventory.quantity,
                    "threshold": threshold,
                    "days_until_stockout": days_left,
                    "supplier": {
                        "id": supplier.id if supplier else None,
                        "name": supplier.name if supplier else None,
                        "contact_email": supplier.contact_email if supplier else None
                    }
                })

    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    })
