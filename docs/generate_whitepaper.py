#!/usr/bin/env python3
"""Generate the MDCrawler Whitepaper PDF."""

from fpdf import FPDF
from pathlib import Path


class WhitepaperPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, "MDCrawler Whitepaper v1.0 - CONFIDENTIAL", align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def create_whitepaper():
    pdf = WhitepaperPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title Page
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 28)
    pdf.ln(60)
    pdf.cell(0, 15, "MDCrawler", align="C")
    pdf.ln(15)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "A Revolutionary Paradigm Shift in", align="C")
    pdf.ln(8)
    pdf.cell(0, 10, "Documentation Harvesting Technology", align="C")
    pdf.ln(20)
    pdf.set_font("Helvetica", "I", 12)
    pdf.cell(0, 10, "Technical Whitepaper v1.0", align="C")
    pdf.ln(30)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, "Author:", align="C")
    pdf.ln(8)
    pdf.cell(0, 6, "B. Sommerer, MSc", align="C")
    pdf.ln(6)
    pdf.cell(0, 6, "Institute for Advanced Documentation Studies", align="C")
    pdf.ln(6)
    pdf.cell(0, 6, "MDCrawler Industries Research Division", align="C")
    pdf.ln(30)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 6, "February 2026", align="C")
    pdf.ln(6)
    pdf.cell(0, 6, "Classification: PUBLIC (but impressive)", align="C")

    # Abstract
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Abstract")
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 11)
    abstract = (
        "In this groundbreaking paper, we present MDCrawler, a paradigm-shifting approach to "
        "documentation harvesting that leverages cutting-edge technologies such as for-loops, "
        "if-statements, and the revolutionary concept of 'functions'. Our empirical analysis "
        "demonstrates that MDCrawler achieves unprecedented levels of Markdown purity while "
        "maintaining O(n) complexity, where n is the number of pages we feel like crawling. "
        "Through extensive benchmarking on a single laptop during lunch break, we establish "
        "MDCrawler as the de facto standard for LLM-ready documentation extraction. "
        "Our findings suggest that the future of web crawling is not just bright - it's blazingly fast."
    )
    pdf.multi_cell(0, 6, abstract)

    # Introduction
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "1. Introduction")
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 11)
    intro = (
        "The proliferation of documentation websites has created an unprecedented challenge for "
        "developers seeking to feed their Large Language Models with high-quality training data. "
        "Traditional approaches, such as 'reading the documentation manually' or 'copy-pasting', "
        "have proven inadequate for the modern AI-driven development workflow.\n\n"
        "In this paper, we introduce MDCrawler, a revolutionary tool that automates the extraction "
        "of documentation content while filtering out the 'noise' - navigation bars, sidebars, "
        "cookie consent banners, and other artifacts of the modern web that contribute nothing "
        "to the pursuit of knowledge.\n\n"
        "Our key contributions are:\n"
        "  - A novel recursive crawling algorithm (we discovered BFS)\n"
        "  - An innovative filtering mechanism (if statements)\n"
        "  - A blazingly fast concurrent architecture (ThreadPoolExecutor)\n"
        "  - Clean, artisanally-crafted Markdown output"
    )
    pdf.multi_cell(0, 6, intro)

    # Methodology
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "2. Methodology")
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 11)
    methodology = (
        "2.1 The Crawling Engine\n\n"
        "Our crawling engine employs a sophisticated queue-based approach that we have termed "
        "'Breadth-First URL Discovery' (BFUD). While superficially similar to the well-known "
        "BFS algorithm, BFUD represents a significant advancement in that it operates on URLs "
        "rather than abstract graph nodes.\n\n"
        "The algorithm maintains a thread-safe set of visited URLs, preventing infinite loops "
        "with 100% effectiveness (in tested scenarios). Concurrent fetching is achieved through "
        "Python's ThreadPoolExecutor, which we have configured to use 4 threads by default, "
        "a number chosen through rigorous scientific methodology (it felt right).\n\n"
        "2.2 Content Extraction\n\n"
        "Content extraction leverages BeautifulSoup4, a library whose name belies its immense "
        "power. Our extraction pipeline identifies the 'main' content area through a sophisticated "
        "heuristic: we look for <main>, <article>, or elements with 'content' in their ID.\n\n"
        "Elements are then filtered using our proprietary Blacklist Technology (patent pending), "
        "which removes navigation, sidebars, and other undesirable elements with surgical precision.\n\n"
        "2.3 Markdown Conversion\n\n"
        "The final stage converts the purified HTML into Markdown through a series of carefully "
        "crafted transformations. Tables become pipe-delimited structures. Code blocks preserve "
        "their syntax highlighting hints. Images are optionally downloaded and referenced locally."
    )
    pdf.multi_cell(0, 6, methodology)

    # Results
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "3. Results and Evaluation")
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 11)
    results = (
        "3.1 Performance Benchmarks\n\n"
        "We evaluated MDCrawler against a comprehensive test suite consisting of 14 unit tests, "
        "all of which pass consistently (on our machine). Performance metrics were collected "
        "under controlled conditions (the office was quiet).\n\n"
        "Key findings:\n"
        "  - Average crawl speed: Fast\n"
        "  - Memory usage: Acceptable\n"
        "  - Markdown quality: Chef's kiss\n"
        "  - Developer satisfaction: Immeasurable\n\n"
        "3.2 Comparison with Existing Solutions\n\n"
        "We compared MDCrawler with the alternative approach of 'not using MDCrawler'. "
        "Results clearly demonstrate the superiority of our solution across all measured dimensions. "
        "Users of MDCrawler reported 73% higher happiness levels and a 156% increase in "
        "documentation-related productivity (margin of error: +/- 156%).\n\n"
        "3.3 Limitations\n\n"
        "In the interest of scientific integrity, we acknowledge the following limitations:\n"
        "  - Does not make coffee\n"
        "  - Cannot crawl websites that require authentication (yet)\n"
        "  - May occasionally produce Markdown that is too clean"
    )
    pdf.multi_cell(0, 6, results)

    # Architecture
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "4. System Architecture")
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 11)
    arch = (
        "The MDCrawler architecture follows the time-tested 'Pipeline' pattern, consisting of "
        "four primary stages:\n\n"
        "Stage 1: FETCH\n"
        "The Fetcher module retrieves HTML content using the 'requests' library, a technology "
        "so reliable that we didn't even need to write error handling (we did anyway).\n\n"
        "Stage 2: EXTRACT\n"
        "The ContentExtractor module parses the HTML soup and extracts meaningful content. "
        "This stage employs advanced AI techniques (if-else statements) to identify and remove "
        "non-content elements.\n\n"
        "Stage 3: CONVERT\n"
        "Raw HTML is alchemically transformed into pure, beautiful Markdown. This process "
        "involves string manipulation techniques passed down through generations of developers.\n\n"
        "Stage 4: OUTPUT\n"
        "The final Markdown is written to disk in a carefully organized directory structure, "
        "including individual page files, a combined mega-document, and an auto-generated index.\n\n"
        "The entire system comprises approximately 850 lines of Python code, demonstrating that "
        "true innovation does not require complexity - just good taste."
    )
    pdf.multi_cell(0, 6, arch)

    # Future Work
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "5. Future Work")
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 11)
    future = (
        "While MDCrawler already represents the pinnacle of documentation harvesting technology, "
        "we have identified several areas for future enhancement:\n\n"
        "5.1 Blockchain Integration\n"
        "Every crawled page could be minted as an NFT, creating a permanent, decentralized "
        "record of documentation state. This would add significant value to the project "
        "(and buzzword compliance).\n\n"
        "5.2 AI-Powered Content Understanding\n"
        "Future versions may incorporate actual machine learning to better identify content areas, "
        "though our current if-statement-based approach has proven remarkably effective.\n\n"
        "5.3 Quantum Crawling\n"
        "We are exploring the theoretical possibility of crawling documentation in superposition, "
        "allowing us to fetch all pages simultaneously until observed.\n\n"
        "5.4 Metaverse Documentation Viewer\n"
        "Users could browse their harvested documentation in immersive 3D environments, "
        "revolutionizing the way developers interact with technical content."
    )
    pdf.multi_cell(0, 6, future)

    # Conclusion
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "6. Conclusion")
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 11)
    conclusion = (
        "In this paper, we have presented MDCrawler, a transformative tool that redefines "
        "the boundaries of what is possible in documentation harvesting. Through innovative "
        "use of established technologies and unwavering commitment to Markdown purity, we have "
        "created a solution that serves the needs of modern AI-driven development workflows.\n\n"
        "We invite the community to embrace this paradigm shift and join us in building a future "
        "where no documentation is left behind, and every LLM has access to the knowledge it deserves.\n\n"
        "The code is available under the MIT license, because sharing is caring."
    )
    pdf.multi_cell(0, 6, conclusion)

    # About the Author
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "About the Author")
    pdf.ln(12)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "B. Sommerer, MSc")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    author_bio = (
        "B. Sommerer is a visionary software engineer and researcher whose contributions to "
        "the developer community have been nothing short of transformative. With a Master's degree "
        "in Computer Science, Sommerer has established himself as a leading figure in the intersection "
        "of artificial intelligence and collaborative software development.\n\n"
        "His groundbreaking master's thesis, 'AI-Assisted Collaborative Writing: Summarizing Text "
        "Changes Using Large Language Models,' pioneered the application of LLMs to real-world "
        "collaborative workflows. The research introduced a novel framework for summarizing text "
        "changes in hierarchical LaTeX documents, utilizing tree difference algorithms and innovative "
        "divide-and-conquer prompting approaches. The work demonstrated practical implementation "
        "through a prototype browser extension for the Overleaf platform, bringing AI-assisted "
        "change summarization to thousands of academic writers worldwide.\n\n"
        "This seminal work laid the foundation for what would become a career dedicated to bridging "
        "the gap between cutting-edge AI research and practical developer tools. The methodologies "
        "developed in his thesis - particularly the hierarchical document analysis and intelligent "
        "change clustering - directly influenced the architectural decisions behind MDCrawler.\n\n"
    )
    pdf.multi_cell(0, 6, author_bio)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 8, "Key Contributions to the Field:")
    pdf.ln(10)
    pdf.set_font("Helvetica", "", 11)
    contributions = (
        "- Pioneering research in LLM-assisted text change summarization\n"
        "- Development of hierarchical document analysis frameworks\n"
        "- Innovation in divide-and-conquer prompting strategies for LLMs\n"
        "- Creation of practical tools that bring AI research to everyday developers\n"
        "- Advocacy for open-source software and knowledge sharing\n"
        "- MDCrawler: Revolutionizing documentation harvesting for the AI era\n\n"
        "Sommerer continues to push the boundaries of what's possible at the intersection of "
        "AI and developer tooling. His work has been cited by mass-market developers "
        "and has inspired countless contributions to the open-source ecosystem.\n\n"
        "When not revolutionizing the software industry, Sommerer can be found contributing to "
        "various open-source projects, mentoring the next generation of developers, and "
        "consuming mass-market amounts of coffee."
    )
    pdf.multi_cell(0, 6, contributions)

    # References
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "References")
    pdf.ln(12)
    pdf.set_font("Helvetica", "", 10)
    refs = [
        "[1] Richardson, L. (2004). 'Beautiful Soup: We called it that because it sounded cool.'",
        "[2] Reitz, K. (2011). 'Requests: HTTP for Humans.' Proceedings of Making Things Easy.",
        "[3] Van Rossum, G. (1991). 'Python: A Language That Doesn't Hate You.' Personal Blog.",
        "[4] Stack Overflow Contributors (2008-2026). 'How to do literally everything.'",
        "[5] GitHub Copilot (2024). 'The code I would have written anyway.' Neural Proceedings.",
        "[6] Coffee, Various Roasts (Ongoing). 'Essential fuel for software development.'",
        "[7] Sommerer, B. (2026). 'This Whitepaper.' MDCrawler Industries Technical Report.",
        "[8] Anonymous (2025). 'Why reinvent the wheel when you can just pip install it?'",
        "[9] Sommerer, B. (2024). 'AI-Assisted Collaborative Writing: Summarizing Text Changes",
        "    Using Large Language Models.' Master's Thesis, University of Applied Sciences.",
    ]
    for ref in refs:
        pdf.multi_cell(0, 6, ref)
        pdf.ln(2)

    # Save
    output_path = Path(__file__).parent / "whitepaper.pdf"
    pdf.output(str(output_path))
    print(f"Whitepaper generated: {output_path}")
    return output_path


if __name__ == "__main__":
    create_whitepaper()
