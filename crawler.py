name: 爬取课文资料

on:
  workflow_dispatch:
    inputs:
      lesson_name:
        description: '课文名称'
        required: true
        type: string

jobs:
  crawl:
    runs-on: ubuntu-latest
    permissions:
      contents: write
    
    steps:
      - name: 检出代码
        uses: actions/checkout@v4
      
      - name: 设置 Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.9'
      
      - name: 安装依赖
        run: |
          pip install requests beautifulsoup4
      
      - name: 运行爬虫
        env:
          LESSON_NAME: ${{ github.event.inputs.lesson_name }}
          DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}
        run: |
          python crawler.py "$LESSON_NAME"
      
      - name: 提交结果
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add data/
          git diff --quiet && git diff --staged --quiet || git commit -m "爬取: ${{ github.event.inputs.lesson_name }}"
          git push
