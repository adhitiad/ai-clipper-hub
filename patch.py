import re

with open(".github/workflows/webpack.yml", "r") as f:
    content = f.read()

# Remove node 18.x from matrix
content = content.replace("node-version: [18.x, 20.x, 22.x]", "node-version: [20.x, 22.x]")

# Update build step with correct working directory and command
build_step_old = """    - name: Build
      run: |
        npm install
        npx webpack"""

build_step_new = """    - name: Build
      working-directory: ./ts-frontend
      run: |
        npm install
        npm run build"""

content = content.replace(build_step_old, build_step_new)

with open(".github/workflows/webpack.yml", "w") as f:
    f.write(content)
