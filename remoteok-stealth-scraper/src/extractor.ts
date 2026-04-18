/**
 * stealth/extractor.ts - Job data extraction from RemoteOK
 */

export interface JobData {
  title: string;
  company: string;
  location: string;
  tags: string[];
  salary: string;
  description: string;
  url: string;
  scrapedAt: string;
  source: string;
  isAI?: boolean;
  [key: string]: any;
}

export interface ExtractionResult {
  allJobs: JobData[];
  aiJobs: JobData[];
  total: number;
  aiCount: number;
}

/**
 * AI-related keywords to filter jobs
 */
const AI_KEYWORDS = [
  'ai',
  'artificial intelligence',
  'machine learning',
  'ml',
  'deep learning',
  'neural network',
  'llm',
  'large language model',
  'nlp',
  'natural language processing',
  'computer vision',
  'data science',
  'ai engineer',
  'ml engineer',
  'deepmind',
  'openai',
  'huggingface',
  'stable diffusion',
  'bert',
  'transformer',
];

/**
 * Check if a job is AI-related
 */
export function isAIJob(job: JobData): boolean {
  const textToCheck = `${job.title}
${job.description}
${job.tags.join(' ')}
${job.company}
${job.location}`.toLowerCase();

  const keywordMatch = AI_KEYWORDS.some((keyword) =>
    textToCheck.includes(keyword.toLowerCase())
  );

  // Also check for AI-related companies
  const companyMatch =
    job.company.toLowerCase().includes('deepmind') ||
    job.company.toLowerCase().includes('openai') ||
    job.company.toLowerCase().includes('huggingface') ||
    job.company.toLowerCase().includes('stable diffusion');

  return keywordMatch || companyMatch;
}

/**
 * Extract job data from a job row element
 */
export async function extractJobData(row: Element): Promise<JobData | null> {
  try {
    // Find job title
    const titleElement = row
      .querySelector('h2, [itemprop="title"], .job-title')
      ?.textContent.trim();
    const title = titleElement || '';

    if (!title) return null;

    // Find company
    const companyElement = row
      .querySelector(
        '[itemprop="hiringOrganization"], .company, [itemprop="organization"]'
      )
      ?.textContent.trim();
    const company = companyElement || 'Unknown';

    // Find location
    const locationElement = row
      .querySelector(
        '[itemprop="jobLocation"], .location, .location-name'
      )
      ?.textContent.trim();
    const location = locationElement || 'Remote';

    // Find tags
    const tagElements = row.querySelectorAll('.tag, .job-tags, .skill-tags');
    const tags = Array.from(tagElements)
      .map((tag) => tag.textContent.trim())
      .filter((tag) => tag.length > 0);

    // Find salary (if available)
    let salary = '';
    const salaryText = row.textContent;

    // Match salary patterns
    const salaryRegex =
      /\$[\d,]+\.?\d{0,2}\s*(?:\-\s*\$[\d,]+\.?\d{0,2})?/g;
    const matches = salaryText.match(salaryRegex);
    if (matches && matches.length > 0) {
      salary = matches[0];
    }

    // Find description from JSON-LD if available
    let description = '';
    const jsonLdScript = row.querySelector('script[type="application/ld+json"]');
    if (jsonLdScript) {
      try {
        const json = JSON.parse(jsonLdScript.textContent);
        if (json.description) {
          description = json.description.substring(0, 1000);
        }
      } catch (e) {
        // Could not parse JSON
      }
    }

    // Find apply URL
    const applyLink = row.querySelector(
      'a[href*="/remote-jobs/"]'
    )?.href || '';
    const url = applyLink;

    return {
      title,
      company,
      location,
      tags,
      salary,
      description: description || title + ' ...',
      url,
      scrapedAt: new Date().toISOString(),
      source: 'RemoteOK',
    };
  } catch (error) {
    console.error('Error parsing job row:', error);
    return null;
  }
}

/**
 * Extract all jobs from a page
 */
export async function extractJobsFromPage(page: Page): Promise<ExtractionResult> {
  console.log('Extracting job data from page...');

  // Wait for jobs to load
  await page.waitForSelector('tr.job, .job-item, [data-job-id]', {
    timeout: 10000,
  }).catch(() => {
    console.log('No job rows found with standard selectors');
  });

  // Extract job data using appropriate selector
  let jobRows; try {
    jobRows = await page.$$eval(
      'tr.job, .job-item, [data-job-id]',
      (rows: Element[]) => rows
    );
  } catch (e) {
    // Fallback to text-based extraction
    jobRows = [];
  }

  if (jobRows.length === 0) {
    console.log('No job rows found');
    return {
      allJobs: [],
      aiJobs: [],
      total: 0,
      aiCount: 0,
    };
  }

  const jobs: JobData[] = await Promise.all(
    jobRows.map((row: Element) => extractJobData(row))
  );

  // Filter out null values
  const validJobs = jobs.filter((job) => job !== null);

  console.log(`Extracted ${validJobs.length} jobs from page`);

  // Filter AI-related jobs
  const aiJobs = validJobs.filter((job) => isAIJob(job));

  aiJobs.forEach((job) => {
    (job as any).isAI = true;
  });

  console.log(`Found ${aiJobs.length} AI-related jobs`);

  return {
    allJobs: validJobs,
    aiJobs: aiJobs,
    total: validJobs.length,
    aiCount: aiJobs.length,
  };
}

/**
 * Parse job data from text content (fallback)
 */
export async function parseFromText(text: string): Promise<JobData[]> {
  // This is a fallback for when structured extraction fails
  // In practice, we rely on DOM parsing
  return [];
}

/**
 * Validate extracted job data
 */
export function validateJob(job: JobData): boolean {
  return (
    job.title.length > 0 &&
    job.company.length > 0 &&
    job.url.length > 0
  );
}