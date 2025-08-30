#!/usr/bin/env node

/**
 * Snyk Advisor Package Health Scraper
 * 
 * This script uses Playwright to fetch and parse package health data from Snyk Advisor.
 * It's designed to be used by the Package Health Reviewer agent.
 * 
 * Usage:
 *   node snyk-advisor-scraper.js <package-name> [registry]
 * 
 * Example:
 *   node snyk-advisor-scraper.js express npm
 *   node snyk-advisor-scraper.js request npm
 */

const { chromium } = require('playwright');

async function scrapePackageHealth(packageName, registry = 'npm') {
  const browser = await chromium.launch({ 
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--no-first-run',
      '--no-zygote',
      '--disable-gpu'
    ]
  });
  
  const page = await browser.newPage();
  
  // Set realistic headers to avoid bot detection
  await page.setExtraHTTPHeaders({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
  });
  
  try {
    const url = `https://snyk.io/advisor/${registry}-package/${packageName}`;
    console.error(`Fetching: ${url}`);
    
    // Navigate with timeout and wait for network to be idle
    await page.goto(url, { 
      waitUntil: 'networkidle',
      timeout: 30000 
    });
    
    // Wait for the main content to load
    await page.waitForSelector('[data-testid="package-header"]', { timeout: 10000 });
    
    // Extract package health metrics
    const metrics = await page.evaluate(() => {
      const result = {
        packageName: '',
        exists: false,
        deprecated: false,
        securityScore: null,
        popularityScore: null,
        maintenanceScore: null,
        communityScore: null,
        overallScore: null,
        vulnerabilities: {
          critical: 0,
          high: 0,
          medium: 0,
          low: 0,
          total: 0
        },
        popularity: {
          weeklyDownloads: '',
          githubStars: 0,
          dependents: 0
        },
        maintenance: {
          lastUpdate: '',
          updateFrequency: '',
          maintainerResponse: ''
        },
        community: {
          githubActivity: '',
          documentation: '',
          issues: 0
        },
        recommendations: [],
        alternatives: [],
        rawData: {}
      };
      
      try {
        // Check if package exists
        const notFoundIndicator = document.querySelector('[data-testid="not-found"]') || 
                                 document.querySelector('.not-found') ||
                                 document.body.textContent.includes('Package not found');
        
        if (notFoundIndicator) {
          return { ...result, error: 'Package not found' };
        }
        
        result.exists = true;
        
        // Extract package name
        const packageHeader = document.querySelector('[data-testid="package-header"]') ||
                             document.querySelector('h1') ||
                             document.querySelector('.package-name');
        if (packageHeader) {
          result.packageName = packageHeader.textContent.trim();
        }
        
        // Check for deprecation warning
        const deprecationWarning = document.querySelector('[data-testid="deprecation-warning"]') ||
                                  document.querySelector('.deprecation') ||
                                  Array.from(document.querySelectorAll('*')).find(el => 
                                    el.textContent.toLowerCase().includes('deprecated'));
        result.deprecated = !!deprecationWarning;
        
        // Extract overall score (usually displayed prominently)
        const scoreElements = document.querySelectorAll('[data-testid*="score"], .score, .rating');
        for (const element of scoreElements) {
          const text = element.textContent;
          const scoreMatch = text.match(/(\d+)\/100|(\d+)%|(\d+\.\d+)/);
          if (scoreMatch) {
            result.overallScore = parseInt(scoreMatch[1] || scoreMatch[2] || scoreMatch[3]);
            break;
          }
        }
        
        // Extract security vulnerabilities
        const vulnElements = document.querySelectorAll('[data-testid*="vulnerability"], .vulnerability, .security');
        for (const element of vulnElements) {
          const text = element.textContent.toLowerCase();
          
          // Look for vulnerability counts
          const criticalMatch = text.match(/(\d+)\s*critical/);
          const highMatch = text.match(/(\d+)\s*high/);
          const mediumMatch = text.match(/(\d+)\s*medium/);
          const lowMatch = text.match(/(\d+)\s*low/);
          
          if (criticalMatch) result.vulnerabilities.critical = parseInt(criticalMatch[1]);
          if (highMatch) result.vulnerabilities.high = parseInt(highMatch[1]);
          if (mediumMatch) result.vulnerabilities.medium = parseInt(mediumMatch[1]);
          if (lowMatch) result.vulnerabilities.low = parseInt(lowMatch[1]);
        }
        
        result.vulnerabilities.total = result.vulnerabilities.critical + 
                                      result.vulnerabilities.high + 
                                      result.vulnerabilities.medium + 
                                      result.vulnerabilities.low;
        
        // Extract popularity metrics
        const downloadElements = document.querySelectorAll('[data-testid*="download"], .downloads, .popularity');
        for (const element of downloadElements) {
          const text = element.textContent;
          const downloadMatch = text.match(/([\d,]+[KMB]?)\s*(weekly|downloads)/i);
          if (downloadMatch) {
            result.popularity.weeklyDownloads = downloadMatch[1];
            break;
          }
        }
        
        // Extract GitHub stars
        const starElements = document.querySelectorAll('[data-testid*="star"], .stars, .github');
        for (const element of starElements) {
          const text = element.textContent;
          const starMatch = text.match(/([\d,]+)\s*stars?/i);
          if (starMatch) {
            result.popularity.githubStars = parseInt(starMatch[1].replace(/,/g, ''));
            break;
          }
        }
        
        // Extract maintenance information
        const maintenanceElements = document.querySelectorAll('[data-testid*="maintenance"], .maintenance, .updated');
        for (const element of maintenanceElements) {
          const text = element.textContent;
          
          // Look for last update date
          const dateMatch = text.match(/(\d{4}-\d{2}-\d{2}|\d+\s*(days?|months?|years?)\s*ago)/i);
          if (dateMatch) {
            result.maintenance.lastUpdate = dateMatch[1];
          }
          
          // Look for maintenance frequency indicators
          if (text.toLowerCase().includes('regular')) {
            result.maintenance.updateFrequency = 'regular';
          } else if (text.toLowerCase().includes('infrequent')) {
            result.maintenance.updateFrequency = 'infrequent';
          }
        }
        
        // Extract individual scores if available
        const scoreCards = document.querySelectorAll('.score-card, [data-testid*="score-card"]');
        scoreCards.forEach(card => {
          const text = card.textContent.toLowerCase();
          const scoreMatch = text.match(/(\d+)/);
          const score = scoreMatch ? parseInt(scoreMatch[1]) : null;
          
          if (text.includes('security') && score !== null) {
            result.securityScore = score;
          } else if (text.includes('popularity') && score !== null) {
            result.popularityScore = score;
          } else if (text.includes('maintenance') && score !== null) {
            result.maintenanceScore = score;
          } else if (text.includes('community') && score !== null) {
            result.communityScore = score;
          }
        });
        
        // Extract recommendations and alternatives
        const recommendationElements = document.querySelectorAll('[data-testid*="recommendation"], .recommendation, .alternative');
        recommendationElements.forEach(element => {
          const text = element.textContent.trim();
          if (text && text.length > 10) {
            if (element.textContent.toLowerCase().includes('alternative')) {
              result.alternatives.push(text);
            } else {
              result.recommendations.push(text);
            }
          }
        });
        
        // Store raw data for debugging
        result.rawData = {
          title: document.title,
          url: window.location.href,
          hasScoreCards: scoreCards.length > 0,
          hasVulnerabilities: vulnElements.length > 0,
          hasPopularityData: downloadElements.length > 0
        };
        
        return result;
        
      } catch (error) {
        return { ...result, error: error.message };
      }
    });
    
    return metrics;
    
  } catch (error) {
    throw new Error(`Failed to scrape package data: ${error.message}`);
  } finally {
    await browser.close();
  }
}

// Calculate health score based on extracted metrics
function calculateHealthScore(metrics) {
  if (!metrics.exists || metrics.error) {
    return {
      healthScore: 'error',
      overallScore: 0,
      reasoning: metrics.error || 'Package analysis failed'
    };
  }
  
  let score = 0;
  const factors = [];
  
  // Security factor (40% weight)
  if (metrics.vulnerabilities.critical > 0) {
    score -= 40;
    factors.push(`Critical vulnerabilities: ${metrics.vulnerabilities.critical}`);
  } else if (metrics.vulnerabilities.high > 0) {
    score -= 20;
    factors.push(`High vulnerabilities: ${metrics.vulnerabilities.high}`);
  } else if (metrics.vulnerabilities.medium > 0) {
    score -= 10;
    factors.push(`Medium vulnerabilities: ${metrics.vulnerabilities.medium}`);
  } else {
    score += 40;
    factors.push('No critical/high vulnerabilities');
  }
  
  // Deprecation factor (30% weight)
  if (metrics.deprecated) {
    score -= 30;
    factors.push('Package is deprecated');
  } else {
    score += 30;
    factors.push('Package is actively maintained');
  }
  
  // Popularity factor (20% weight)
  const downloads = metrics.popularity.weeklyDownloads;
  if (downloads) {
    const downloadNum = parseFloat(downloads.replace(/[KMB,]/g, ''));
    const multiplier = downloads.includes('M') ? 1000000 : 
                      downloads.includes('K') ? 1000 : 1;
    const weeklyDownloads = downloadNum * multiplier;
    
    if (weeklyDownloads > 100000) {
      score += 20;
      factors.push(`High popularity: ${downloads} weekly downloads`);
    } else if (weeklyDownloads > 10000) {
      score += 10;
      factors.push(`Moderate popularity: ${downloads} weekly downloads`);
    } else {
      factors.push(`Low popularity: ${downloads} weekly downloads`);
    }
  }
  
  // Maintenance factor (10% weight)
  if (metrics.maintenance.lastUpdate) {
    const updateText = metrics.maintenance.lastUpdate.toLowerCase();
    if (updateText.includes('days ago') || updateText.includes('weeks ago')) {
      score += 10;
      factors.push('Recently updated');
    } else if (updateText.includes('months ago')) {
      score += 5;
      factors.push('Updated within months');
    } else {
      factors.push('Not recently updated');
    }
  }
  
  // Ensure score is within bounds
  score = Math.max(0, Math.min(100, score + 50)); // Base score of 50
  
  // Determine health category
  let healthScore;
  if (score >= 90) {
    healthScore = 'healthy';
  } else if (score >= 60) {
    healthScore = 'sustainable';
  } else {
    healthScore = 'risky';
  }
  
  return {
    healthScore,
    overallScore: score,
    reasoning: factors.join('; ')
  };
}

// Main execution
async function main() {
  const packageName = process.argv[2];
  const registry = process.argv[3] || 'npm';
  
  if (!packageName) {
    console.error('Usage: node snyk-advisor-scraper.js <package-name> [registry]');
    process.exit(1);
  }
  
  try {
    console.error(`Analyzing package: ${packageName} (${registry})`);
    
    const metrics = await scrapePackageHealth(packageName, registry);
    const healthAssessment = calculateHealthScore(metrics);
    
    // Combine results
    const result = {
      health_score: healthAssessment.healthScore,
      package_name: packageName,
      registry: registry,
      overall_score: healthAssessment.overallScore,
      assessment_date: new Date().toISOString(),
      security_metrics: metrics.vulnerabilities,
      popularity_metrics: metrics.popularity,
      maintenance_metrics: metrics.maintenance,
      community_metrics: metrics.community,
      recommendations: metrics.recommendations.length > 0 ? metrics.recommendations : 
        generateRecommendations(healthAssessment.healthScore, metrics),
      alternatives: metrics.alternatives,
      snyk_url: `https://snyk.io/advisor/${registry}-package/${packageName}`,
      analysis_summary: generateSummary(healthAssessment, metrics),
      raw_metrics: metrics
    };
    
    // Output JSON result
    console.log(JSON.stringify(result, null, 2));
    
  } catch (error) {
    console.error(`Error: ${error.message}`);
    
    const errorResult = {
      health_score: 'error',
      package_name: packageName,
      registry: registry,
      overall_score: 0,
      assessment_date: new Date().toISOString(),
      error: error.message,
      analysis_summary: `Failed to analyze package ${packageName}: ${error.message}`
    };
    
    console.log(JSON.stringify(errorResult, null, 2));
    process.exit(1);
  }
}

function generateRecommendations(healthScore, metrics) {
  const recommendations = [];
  
  switch (healthScore) {
    case 'healthy':
      recommendations.push('Safe to use in production environments');
      recommendations.push('Keep updated to latest version');
      recommendations.push('Excellent choice for new projects');
      break;
      
    case 'sustainable':
      recommendations.push('Generally safe to use with monitoring');
      recommendations.push('Review security updates regularly');
      recommendations.push('Consider alternatives for critical applications');
      break;
      
    case 'risky':
      recommendations.push('⚠️ Use with caution or avoid entirely');
      recommendations.push('Review security vulnerabilities carefully');
      recommendations.push('Consider migration to safer alternatives');
      
      if (metrics.deprecated) {
        recommendations.push('Package is deprecated - migration strongly recommended');
      }
      
      if (metrics.vulnerabilities.critical > 0) {
        recommendations.push('Critical security vulnerabilities present');
      }
      break;
      
    case 'error':
      recommendations.push('Unable to assess package health');
      recommendations.push('Manual review required');
      break;
  }
  
  return recommendations;
}

function generateSummary(healthAssessment, metrics) {
  const { healthScore, overallScore, reasoning } = healthAssessment;
  const packageName = metrics.packageName || 'Unknown package';
  
  let summary = `${packageName} is a ${healthScore} package with a score of ${overallScore}/100. `;
  
  if (metrics.deprecated) {
    summary += 'This package is deprecated and should be avoided. ';
  }
  
  if (metrics.vulnerabilities.total > 0) {
    summary += `It has ${metrics.vulnerabilities.total} known vulnerabilities. `;
  }
  
  if (metrics.popularity.weeklyDownloads) {
    summary += `Weekly downloads: ${metrics.popularity.weeklyDownloads}. `;
  }
  
  summary += reasoning;
  
  return summary;
}

// Run the script
if (require.main === module) {
  main();
}

module.exports = { scrapePackageHealth, calculateHealthScore };