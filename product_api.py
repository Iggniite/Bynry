
# Endpoint to create a new product and its initial inventory
@app.route('/api/products', methods=['POST'])
def create_product():
    # Parse JSON payload from incoming POST request
    data = request.get_json()

    # Step 1: Validate required fields
    # Define fields that are absolutely required to create a product

    required_fields = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']

    # Check which required fields are missing in the request body
    missing = [field for field in required_fields if field not in data]
    if missing:
        # Return a 400 Bad Request with a list of missing fields
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # Step 2: Enforce SKU uniqueness
    # Ensure the SKU does not already exist in the system

    if Product.query.filter_by(sku=data['sku']).first():
        return jsonify({"error": "SKU already exists"}), 400

    try:
        # Step 3: Use a single transaction for both inserts
        # This ensures atomicity — either both product and inventory are saved, or neither
        with db.session.begin():

            # Create new Product instance
            product = Product(
                name=data['name'],
                sku=data['sku'],
                price=Decimal(str(data['price']))  # Safely convert price to Decimal for accuracy
                # Note: No warehouse_id here, as a product can exist in multiple warehouses
            )
            db.session.add(product)

            # Flush sends SQL to DB to generate product.id, without committing yet
            db.session.flush()


            # Create initial inventory entry for the warehouse
            inventory = Inventory(
                product_id=product.id,                  # Link inventory to newly created product
                warehouse_id=data['warehouse_id'],      # Assign to specific warehouse
                quantity=data['initial_quantity']       # Set initial stock level
            )
            db.session.add(inventory)

        # Step 4: Return success response
        # After successful transaction, return JSON response with product ID
        return jsonify({
            "message": "Product created",
            "product_id": product.id
        }), 201  # HTTP 201 Created

    # Step 5: Error Handling
    except IntegrityError:
        # Catches known DB issues (e.g., constraint violations)
        db.session.rollback()  # Undo the partial transaction to keep DB clean
        return jsonify({"error": "Database constraint failed"}), 500

    except Exception as e:
        # Catches any other unexpected errors (e.g., type conversion issues)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500  # Useful for debugging, but avoid in production logs
